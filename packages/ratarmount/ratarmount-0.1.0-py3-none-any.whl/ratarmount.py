#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io
import itertools
import os
import re
import stat
import tarfile
import time
import traceback
from collections import namedtuple
from timeit import default_timer as timer

import fuse


printDebug = 1

def overrides( parentClass ):
    def overrider( method ):
        assert method.__name__ in dir( parentClass )
        return method
    return overrider


FileInfo = namedtuple( "FileInfo", "offset size mtime mode type linkname uid gid istar" )


class ProgressBar:
    def __init__( self, maxValue ):
        self.maxValue = maxValue
        self.lastUpdateTime = time.time()
        self.lastUpdateValue = 0
        self.updateInterval = 2 # seconds
        self.creationTime = time.time()

    def update( self, value ):
        if self.lastUpdateTime is not None and ( time.time() - self.lastUpdateTime ) < self.updateInterval:
            return

        # Use whole interval since start to estimate time
        eta1 = int( ( time.time() - self.creationTime ) / value * ( self.maxValue - value ) )
        # Use only a shorter window interval to estimate time.
        # Accounts better for higher speeds in beginning, e.g., caused by caching effects.
        # However, this estimate might vary a lot while the other one stabilizes after some time!
        eta2 = int( ( time.time() - self.lastUpdateTime ) / ( value - self.lastUpdateValue ) * ( self.maxValue - value ) )
        print( "Currently at position {} of {} ({:.2f}%). "
               "Estimated time remaining with current rate: {} min {} s, with average rate: {} min {} s."
               .format( value, self.maxValue, value / self.maxValue * 100.,
                        eta2 // 60, eta2 % 60,
                        eta1 // 60, eta1 % 60 ),
               flush = True )

        self.lastUpdateTime = time.time()
        self.lastUpdateValue = value

class IndexedTar:
    """
    This class reads once through the whole TAR archive and stores TAR file offsets
    for all contained files in an index to support fast seeking to a given file.
    """

    __slots__ = (
        'tarFileName',
        'fileIndex',
        'mountRecursively',
        'cacheFolder',
        'possibleIndexFilePaths',
        'indexFileName',
        'progressBar',
    )

    # these allowed backends also double as extensions for the index file to look for
    availableSerializationBackends = [
        'none',
        'pickle',
        'pickle2',
        'pickle3',
        'custom',
        'cbor',
        'msgpack',
        'rapidjson',
        'ujson',
        'simplejson'
    ]
    availableCompressions = [
        '', # no compression
        'lz4',
        'gz',
    ]

    def __init__( self,
                  pathToTar = None,
                  fileObject = None,
                  writeIndex = False,
                  clearIndexCache = False,
                  recursive = False,
                  serializationBackend = None,
                  progressBar = None ):
        self.progressBar = progressBar
        self.tarFileName = os.path.normpath( pathToTar )

        # Stores the file hierarchy in a dictionary with keys being either
        #  - the file and containing file metainformation
        #  - or keys being a folder name and containing a recursively defined dictionary.
        self.fileIndex = {}
        self.mountRecursively = recursive

        # will be used for storing indexes if current path is read-only
        self.cacheFolder = os.path.expanduser( "~/.ratarmount" )
        self.possibleIndexFilePaths = [
            self.tarFileName + ".index",
            self.cacheFolder + "/" + self.tarFileName.replace( "/", "_" ) + ".index"
        ]

        if not serializationBackend:
            serializationBackend = 'custom'

        if serializationBackend not in self.supportedIndexExtensions():
            print( "[Warning] Serialization backend '" + str( serializationBackend ) + "' not supported.",
                   "Defaulting to '" + serializationBackend + "'!" )
            print( "List of supported extensions / backends:", self.supportedIndexExtensions() )

            serializationBackend = 'custom'

        # this is the actual index file, which will be used in the end, and by default
        self.indexFileName = self.possibleIndexFilePaths[0] + "." + serializationBackend

        if clearIndexCache:
            for indexPath in self.possibleIndexFilePaths:
                for extension in self.supportedIndexExtensions():
                    indexPathWitExt = indexPath + "." + extension
                    if os.path.isfile( indexPathWitExt ):
                        os.remove( indexPathWitExt )

        if fileObject is not None:
            if writeIndex:
                print( "Can't write out index for file object input. Ignoring this option." )
            self.createIndex( fileObject )
        else:
            # first try loading the index for the given serialization backend
            if serializationBackend is not None:
                for indexPath in self.possibleIndexFilePaths:
                    if self.tryLoadIndex( indexPath + "." + serializationBackend ):
                        break

            # try loading the index from one of the pre-configured paths
            for indexPath in self.possibleIndexFilePaths:
                for extension in self.supportedIndexExtensions():
                    if self.tryLoadIndex( indexPath + "." + extension ):
                        break

            if not self.indexIsLoaded():
                with open( self.tarFileName, 'rb' ) as file:
                    self.createIndex( file )

                if writeIndex:
                    for indexPath in self.possibleIndexFilePaths:
                        indexPath += "." + serializationBackend

                        try:
                            folder = os.path.dirname( indexPath )
                            if not os.path.exists( folder ):
                                os.mkdir( folder )

                            f = open( indexPath, 'wb' )
                            f.close()
                            os.remove( indexPath )
                            self.indexFileName = indexPath

                            break
                        except IOError:
                            if printDebug >= 2:
                                print( "Could not create file:", indexPath )

                    try:
                        self.writeIndex( self.indexFileName )
                    except IOError:
                        print( "[Info] Could not write TAR index to file. ",
                               "Subsequent mounts might be slow!" )

    @staticmethod
    def supportedIndexExtensions():
        return [ '.'.join( combination ).strip( '.' )
                 for combination in itertools.product( IndexedTar.availableSerializationBackends,
                                                       IndexedTar.availableCompressions ) ]
    @staticmethod
    def dump( toDump, file ):
        import msgpack

        if isinstance( toDump, dict ):
            file.write( b'\x01' ) # magic code meaning "start dictionary object"

            for key, value in toDump.items():
                file.write( b'\x03' ) # magic code meaning "serialized key value pair"
                IndexedTar.dump( key, file )
                IndexedTar.dump( value, file )

            file.write( b'\x02' ) # magic code meaning "close dictionary object"

        elif isinstance( toDump, FileInfo ):
            serialized = msgpack.dumps( toDump )
            file.write( b'\x05' ) # magic code meaning "msgpack object"
            file.write( len( serialized ).to_bytes( 4, byteorder = 'little' ) )
            file.write( serialized )

        elif isinstance( toDump, str ):
            serialized = toDump.encode()
            file.write( b'\x04' ) # magic code meaning "string object"
            file.write( len( serialized ).to_bytes( 4, byteorder = 'little' ) )
            file.write( serialized )

        else:
            print( "Ignoring unsupported type to write:", toDump )

    @staticmethod
    def load( file ):
        import msgpack

        elementType = file.read( 1 )

        if elementType != b'\x01': # start of dictionary
            raise Exception( 'Custom TAR index loader: invalid file format' )

        result = {}

        dictElementType = file.read( 1 )
        while dictElementType:
            if dictElementType == b'\x02':
                break

            elif dictElementType == b'\x03':
                keyType = file.read( 1 )
                if keyType != b'\x04': # key must be string object
                    raise Exception( 'Custom TAR index loader: invalid file format' )
                size = int.from_bytes( file.read( 4 ), byteorder = 'little' )
                key = file.read( size ).decode()

                valueType = file.read( 1 )
                if valueType == b'\x05': # msgpack object
                    size = int.from_bytes( file.read( 4 ), byteorder = 'little' )
                    serialized = file.read( size )
                    value = FileInfo( *msgpack.loads( serialized ) )

                elif valueType == b'\x01': # dict object
                    file.seek( -1, io.SEEK_CUR )
                    value = IndexedTar.load( file )

                else:
                    raise Exception(
                        'Custom TAR index loader: invalid file format ' +
                        '(expected msgpack or dict but got' +
                        str( int.from_bytes( valueType, byteorder = 'little' ) ) + ')' )

                result[key] = value

            else:
                raise Exception(
                    'Custom TAR index loader: invalid file format ' +
                    '(expected end-of-dict or key-value pair but got' +
                    str( int.from_bytes( dictElementType, byteorder = 'little' ) ) + ')' )

            dictElementType = file.read( 1 )

        return result

    def getFileInfo( self, path, listDir = False ):
        # go down file hierarchy tree along the given path
        p = self.fileIndex
        for name in os.path.normpath( path ).split( os.sep ):
            if not name:
                continue
            if name not in p:
                return None
            p = p[name]

        def repackDeserializedNamedTuple( p ):
            if isinstance( p, list ) and len( p ) == len( FileInfo._fields ):
                return FileInfo( *p )

            if isinstance( p, dict ) and len( p ) == len( FileInfo._fields ) and \
                 'uid' in p and isinstance( p['uid'], int ):
                # a normal directory dict must only have dict or FileInfo values,
                # so if the value to the 'uid' key is an actual int,
                # then it is sure it is a deserialized FileInfo object and not a file named 'uid'
                print( "P ===", p )
                print( "FileInfo ===", FileInfo( **p ) )
                return FileInfo( **p )

            return p

        p = repackDeserializedNamedTuple( p )

        # if the directory contents are not to be printed and it is a directory,
        # return the "file" info of ".", which holds the directory metainformation
        if not listDir and isinstance( p, dict ):
            if '.' in p:
                p = p['.']
            else:
                return FileInfo(
                    offset   = 0, # not necessary for directory anyways
                    size     = 1, # might be misleading / non-conform
                    mtime    = 0,
                    mode     = 0o555 | stat.S_IFDIR,
                    type     = tarfile.DIRTYPE,
                    linkname = "",
                    uid      = 0,
                    gid      = 0,
                    istar    = False
                )

        return repackDeserializedNamedTuple( p )

    def isDir( self, path ):
        return isinstance( self.getFileInfo( path, listDir = True ), dict )

    def exists( self, path ):
        path = os.path.normpath( path )
        return self.isDir( path ) or isinstance( self.getFileInfo( path ), FileInfo )

    def setFileInfo( self, path, fileInfo ):
        """
        path: the full path to the file with leading slash (/) for which to set the file info
        """
        assert isinstance( fileInfo, FileInfo )

        pathHierarchy = os.path.normpath( path ).split( os.sep )
        if not pathHierarchy:
            return

        # go down file hierarchy tree along the given path
        p = self.fileIndex
        for name in pathHierarchy[:-1]:
            if not name:
                continue
            assert isinstance( p, dict )
            p = p.setdefault( name, {} )

        # create a new key in the dictionary of the parent folder
        p.update( { pathHierarchy[-1] : fileInfo } )

    def setDirInfo( self, path, dirInfo, dirContents = {} ):
        """
        path: the full path to the file with leading slash (/) for which to set the folder info
        """
        assert isinstance( dirInfo, FileInfo )
        assert isinstance( dirContents, dict )

        pathHierarchy = os.path.normpath( path ).strip( os.sep ).split( os.sep )
        if not pathHierarchy:
            return

        # go down file hierarchy tree along the given path
        p = self.fileIndex
        for name in pathHierarchy[:-1]:
            if not name:
                continue
            assert isinstance( p, dict )
            p = p.setdefault( name, {} )

        # create a new key in the dictionary of the parent folder
        p.update( { pathHierarchy[-1] : dirContents } )
        p[pathHierarchy[-1]].update( { '.' : dirInfo } )

    def createIndex( self, fileObject ):
        if printDebug >= 1:
            print( "Creating offset dictionary for",
                   "<file object>" if self.tarFileName is None else self.tarFileName, "..." )
        t0 = timer()

        self.fileIndex = {}
        try:
            loadedTarFile = tarfile.open( fileobj = fileObject, mode = 'r:' )
        except tarfile.ReadError as exception:
            print( "Archive can't be opened! This might happen for compressed TAR archives, "
                   "which currently is not supported." )
            raise exception

        if self.progressBar is None and os.path.isfile( self.tarFileName ):
            self.progressBar = ProgressBar( os.stat( self.tarFileName ).st_size )

        for tarInfo in loadedTarFile:
            if self.progressBar is not None:
                self.progressBar.update( tarInfo.offset_data )

            mode = tarInfo.mode
            if tarInfo.isdir() : mode |= stat.S_IFDIR
            if tarInfo.isfile(): mode |= stat.S_IFREG
            if tarInfo.issym() : mode |= stat.S_IFLNK
            if tarInfo.ischr() : mode |= stat.S_IFCHR
            if tarInfo.isfifo(): mode |= stat.S_IFIFO
            fileInfo = FileInfo(
                offset   = tarInfo.offset_data,
                size     = tarInfo.size       ,
                mtime    = tarInfo.mtime      ,
                mode     = mode               ,
                type     = tarInfo.type       ,
                linkname = tarInfo.linkname   ,
                uid      = tarInfo.uid        ,
                gid      = tarInfo.gid        ,
                istar    = False
            )

            # open contained tars for recursive mounting
            indexedTar = None
            if self.mountRecursively and tarInfo.isfile() and tarInfo.name.endswith( ".tar" ):
                oldPos = fileObject.tell()
                if oldPos != tarInfo.offset_data:
                    fileObject.seek( tarInfo.offset_data )
                indexedTar = IndexedTar( tarInfo.name,
                                         fileObject = fileObject,
                                         writeIndex = False,
                                         progressBar = self.progressBar )
                # might be especially necessary if the .tar is not actually a tar!
                fileObject.seek( fileObject.tell() )

            # Add a leading '/' as a convention where '/' represents the TAR root folder
            # Partly, done because fusepy specifies paths in a mounted directory like this
            path = os.path.normpath( "/" + tarInfo.name )

            # test whether the TAR file could be loaded and if so "mount" it recursively
            if indexedTar is not None and indexedTar.indexIsLoaded():
                # actually apply the recursive tar mounting
                extractedName = re.sub( r"\.tar$", "", path )
                if not self.exists( extractedName ):
                    path = extractedName

                mountMode = ( fileInfo.mode & 0o777 ) | stat.S_IFDIR
                if mountMode & stat.S_IRUSR != 0: mountMode |= stat.S_IXUSR
                if mountMode & stat.S_IRGRP != 0: mountMode |= stat.S_IXGRP
                if mountMode & stat.S_IROTH != 0: mountMode |= stat.S_IXOTH
                fileInfo = fileInfo._replace( mode = mountMode, istar = True )

                if self.exists( path ):
                    print( "[Warning]", path, "already exists in database and will be overwritten!" )

                # merge fileIndex from recursively loaded TAR into our Indexes
                self.setDirInfo( path, fileInfo, indexedTar.fileIndex )

            elif path != '/':
                # just a warning and check for the path already existing
                if self.exists( path ):
                    fileInfo = self.getFileInfo( path, listDir = False )
                    if fileInfo.istar:
                        # move recursively mounted TAR directory to original .tar name if there is a name-clash,
                        # e.g., when foo/ also exists in the TAR but foo.tar would be mounted to foo/.
                        # In this case, move that mount to foo.tar/
                        self.setFileInfo( path + ".tar", fileInfo, self.getFileInfo( path, listDir = True ) )
                    else:
                        print( "[Warning]", path, "already exists in database and will be overwritten!" )

                # simply store the file or directory information from current TAR item
                if tarInfo.isdir():
                    self.setDirInfo( path, fileInfo, {} )
                else:
                    self.setFileInfo( path, fileInfo )

        t1 = timer()
        if printDebug >= 1:
            print( "Creating offset dictionary for",
                   "<file object>" if self.tarFileName is None else self.tarFileName,
                   "took {:.2f}s".format( t1 - t0 ) )

    def serializationBackendFromFileName( self, fileName ):
        splitName = fileName.split( '.' )

        if len( splitName ) > 2 and '.'.join( splitName[-2:] ) in self.supportedIndexExtensions():
            return '.'.join( splitName[-2:] )

        if splitName[-1] in self.supportedIndexExtensions():
            return splitName[-1]

        return None

    def indexIsLoaded( self ):
        return bool( self.fileIndex )

    def writeIndex( self, outFileName ):
        """
        outFileName: Full file name with backend extension.
                     Depending on the extension the serialization is chosen.
        """

        serializationBackend = self.serializationBackendFromFileName( outFileName )

        if printDebug >= 1:
            print( "Writing out TAR index using", serializationBackend, "to", outFileName, "..." )
        t0 = timer()

        fileMode = 'wt' if 'json' in serializationBackend else 'wb'

        if serializationBackend.endswith( '.lz4' ):
            import lz4.frame
            wrapperOpen = lambda x : lz4.frame.open( x, fileMode )
        elif serializationBackend.endswith( '.gz' ):
            import gzip
            wrapperOpen = lambda x : gzip.open( x, fileMode )
        else:
            wrapperOpen = lambda x : open( x, fileMode )
        serializationBackend = serializationBackend.split( '.' )[0]

        # libraries tested but not working:
        #  - marshal: can't serialize namedtuples
        #  - hickle: for some reason, creates files almost 64x larger and slower than pickle!?
        #  - yaml: almost a 10 times slower and more memory usage and deserializes everything including ints to string

        if serializationBackend == 'none':
            print( "Won't write out index file because backend 'none' was chosen. "
                   "Subsequent mounts might be slow!" )
            return

        with wrapperOpen( outFileName ) as outFile:
            if serializationBackend == 'pickle2':
                import pickle
                pickle.dump( self.fileIndex, outFile )
                pickle.dump( self.fileIndex, outFile, protocol = 2 )

            # default serialization because it has the fewest dependencies and because it was legacy default
            elif serializationBackend == 'pickle3' or \
                 serializationBackend == 'pickle' or \
                 serializationBackend is None:
                import pickle
                pickle.dump( self.fileIndex, outFile )
                pickle.dump( self.fileIndex, outFile, protocol = 3 ) # 3 is default protocol

            elif serializationBackend == 'simplejson':
                import simplejson
                simplejson.dump( self.fileIndex, outFile, namedtuple_as_object = True )

            elif serializationBackend == 'custom':
                IndexedTar.dump( self.fileIndex, outFile )

            elif serializationBackend in [ 'msgpack', 'cbor', 'rapidjson', 'ujson' ]:
                import importlib
                module = importlib.import_module( serializationBackend )
                getattr( module, 'dump' )( self.fileIndex, outFile )

            else:
                print( "Tried to save index with unsupported extension backend:", serializationBackend, "!" )

        t1 = timer()
        if printDebug >= 1:
            print( "Writing out TAR index to", outFileName, "took {:.2f}s".format( t1 - t0 ),
                   "and is sized", os.stat( outFileName ).st_size, "B" )

    def loadIndex( self, indexFileName ):
        if printDebug >= 1:
            print( "Loading offset dictionary from", indexFileName, "..." )
        t0 = timer()

        serializationBackend = self.serializationBackendFromFileName( indexFileName )

        fileMode = 'rt' if 'json' in serializationBackend else 'rb'

        if serializationBackend.endswith( '.lz4' ):
            import lz4.frame
            wrapperOpen = lambda x : lz4.frame.open( x, fileMode )
        elif serializationBackend.endswith( '.gz' ):
            import gzip
            wrapperOpen = lambda x : gzip.open( x, fileMode )
        else:
            wrapperOpen = lambda x : open( x, fileMode )
        serializationBackend = serializationBackend.split( '.' )[0]

        with wrapperOpen( indexFileName ) as indexFile:
            if serializationBackend in ( 'pickle2', 'pickle3', 'pickle' ):
                import pickle
                self.fileIndex = pickle.load( indexFile )

            elif serializationBackend == 'custom':
                self.fileIndex = IndexedTar.load( indexFile )

            elif serializationBackend == 'msgpack':
                import msgpack
                self.fileIndex = msgpack.load( indexFile, raw = False )

            elif serializationBackend == 'simplejson':
                import simplejson
                self.fileIndex = simplejson.load( indexFile, namedtuple_as_object = True )

            elif serializationBackend in [ 'cbor', 'rapidjson', 'ujson' ]:
                import importlib
                module = importlib.import_module( serializationBackend )
                self.fileIndex = getattr( module, 'load' )( indexFile )

            else:
                print( "Tried to load index path with unsupported serializationBackend:", serializationBackend, "!" )
                return

        if printDebug >= 2:
            def countDictEntries( d ):
                n = 0
                for value in d.values():
                    n += countDictEntries( value ) if isinstance( value, dict ) else 1
                return n
            print( "Files:", countDictEntries( self.fileIndex ) )

        t1 = timer()
        if printDebug >= 1:
            print( "Loading offset dictionary from", indexFileName, "took {:.2f}s".format( t1 - t0 ) )

    def tryLoadIndex( self, indexFileName ):
        """calls loadIndex if index is not loaded already and provides extensive error handling"""

        if self.indexIsLoaded():
            return True

        if not os.path.isfile( indexFileName ):
            return False

        if os.path.getsize( indexFileName ) == 0:
            try:
                os.remove( indexFileName )
            except OSError:
                print( "[Warning] Failed to remove empty old cached index file:", indexFileName )

            return False

        try:
            self.loadIndex( indexFileName )
        except Exception:
            self.fileIndex = None

            traceback.print_exc()
            print( "[Warning] Could not load file '" + indexFileName  )

            print( "[Info] Some likely reasons for not being able to load the index file:" )
            print( "[Info]   - Some dependencies are missing. Please isntall them with:" )
            print( "[Info]       pip3 --user -r requirements.txt" )
            print( "[Info]   - The file has incorrect read permissions" )
            print( "[Info]   - The file got corrupted because of:" )
            print( "[Info]     - The program exited while it was still writing the index because of:" )
            print( "[Info]       - the user sent SIGINT to force the program to quit" )
            print( "[Info]       - an internal error occured while writing the index" )
            print( "[Info]       - the disk filled up while writing the index" )
            print( "[Info]     - Rare lowlevel corruptions caused by hardware failure" )

            print( "[Info] This might force a time-costly index recreation, so if it happens often and "
                   "mounting is slow, try to find out why loading fails repeatedly, "
                   "e.g., by opening an issue on the public github page." )

            try:
                os.remove( indexFileName )
            except OSError:
                print( "[Warning] Failed to remove corrupted old cached index file:", indexFileName )

        return self.indexIsLoaded()


class TarMount( fuse.Operations ):
    """
    This class implements the fusepy interface in order to create a mounted file system view
    to a TAR archive.
    This class can and is relatively thin as it only has to create and manage an IndexedTar
    object and query it for directory or file contents.
    It also adds a layer over the file permissions as all files must be read-only even
    if the TAR reader reports the file as originally writable because no TAR write support
    is planned.
    """

    def __init__( self,
                  pathToMount,
                  clearIndexCache = False,
                  recursive = False,
                  serializationBackend = None,
                  prefix = '' ):
        self.tarFileName = pathToMount
        self.tarFile = open( self.tarFileName, 'rb' )
        self.indexedTar = IndexedTar(
            self.tarFileName,
            writeIndex = True,
            clearIndexCache = clearIndexCache,
            recursive = recursive,
            serializationBackend = serializationBackend )

        if prefix and not self.indexedTar.isDir( prefix ):
            prefix = ''
        if prefix and not prefix.endswith( '/' ):
            prefix += '/'
        self.prefix = prefix

        # make the mount point read only and executable if readable, i.e., allow directory listing
        # @todo In some cases, I even 2(!) '.' directories listed with ls -la!
        #       But without this, the mount directory is owned by root
        tarStats = os.stat( self.tarFileName )
        # clear higher bits like S_IFREG and set the directory bit instead
        mountMode = ( tarStats.st_mode & 0o777 ) | stat.S_IFDIR
        if mountMode & stat.S_IRUSR != 0: mountMode |= stat.S_IXUSR
        if mountMode & stat.S_IRGRP != 0: mountMode |= stat.S_IXGRP
        if mountMode & stat.S_IROTH != 0: mountMode |= stat.S_IXOTH
        self.indexedTar.fileIndex[ self.prefix + '.' ] = FileInfo(
            offset   = 0                ,
            size     = tarStats.st_size ,
            mtime    = tarStats.st_mtime,
            mode     = mountMode        ,
            type     = tarfile.DIRTYPE  ,
            linkname = ""               ,
            uid      = tarStats.st_uid  ,
            gid      = tarStats.st_gid  ,
            istar    = True
        )

        if printDebug >= 3:
            print( "Loaded File Index:", self.indexedTar.fileIndex )

    @overrides( fuse.Operations )
    def getattr( self, path, fh = None ):
        if printDebug >= 2:
            print( "[getattr( path =", path, ", fh =", fh, ")] Enter" )

        fileInfo = self.indexedTar.getFileInfo( self.prefix + path, listDir = False )
        if not isinstance( fileInfo, FileInfo ):
            if printDebug >= 2:
                print( "Could not find path:", path )
            raise fuse.FuseOSError( fuse.errno.EROFS )

        # dictionary keys: https://pubs.opengroup.org/onlinepubs/007904875/basedefs/sys/stat.h.html
        statDict = dict( ( "st_" + key, getattr( fileInfo, key ) ) for key in ( 'size', 'mtime', 'mode', 'uid', 'gid' ) )
        # signal that everything was mounted read-only
        statDict['st_mode'] &= ~( stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH )
        statDict['st_mtime'] = int( statDict['st_mtime'] )
        statDict['st_nlink'] = 2

        if printDebug >= 2:
            print( "[getattr( path =", path, ", fh =", fh, ")] return:", statDict )

        return statDict

    @overrides( fuse.Operations )
    def readdir( self, path, fh ):
        if printDebug >= 2:
            print( "[readdir( path =", path, ", fh =", fh, ")] return:",
                   self.indexedTar.getFileInfo( self.prefix + path, listDir = True ).keys() )

        # we only need to return these special directories. FUSE automatically expands these and will not ask
        # for paths like /../foo/./../bar, so we don't need to worry about cleaning such paths
        yield '.'
        yield '..'

        for key in self.indexedTar.getFileInfo( self.prefix + path, listDir = True ).keys():
            yield key

    @overrides( fuse.Operations )
    def readlink( self, path ):
        if printDebug >= 2:
            print( "[readlink( path =", path, ")]" )

        fileInfo = self.indexedTar.getFileInfo( self.prefix + path )
        if not isinstance( fileInfo, FileInfo ):
            raise fuse.FuseOSError( fuse.errno.EROFS )

        pathname = fileInfo.linkname
        if pathname.startswith( "/" ):
            return os.path.relpath( pathname, "/" ) # @todo Not exactly sure what to return here

        return pathname

    @overrides( fuse.Operations )
    def read( self, path, length, offset, fh ):
        if printDebug >= 2:
            print( "[read( path =", path, ", length =", length, ", offset =", offset, ",fh =", fh, ")] path:", path )

        fileInfo = self.indexedTar.getFileInfo( self.prefix + path )
        if not isinstance( fileInfo, FileInfo ):
            raise fuse.FuseOSError( fuse.errno.EROFS )

        self.tarFile.seek( fileInfo.offset + offset, os.SEEK_SET )
        return self.tarFile.read( length )


def cli():
    parser = argparse.ArgumentParser(
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
        description = '''\
        If no mount path is specified, then the tar will be mounted to a folder of the same name but without a file extension.
        TAR files contained inside the tar and even TARs in TARs in TARs will be mounted recursively at folders of the same name barred the file extension '.tar'.

        In order to reduce the mounting time, the created index for random access to files inside the tar will be saved to <path to tar>.index.<backend>[.<compression]. If it can't be saved there, it will be saved in ~/.ratarmount/<path to tar: '/' -> '_'>.index.<backend>[.<compression].
        ''' )

    parser.add_argument(
        '-f', '--foreground', action='store_true', default = False,
        help = 'keeps the python program in foreground so it can print debug'
               'output when the mounted path is accessed.' )

    parser.add_argument(
        '-d', '--debug', type = int, default = 1,
        help = 'sets the debugging level. Higher means more output. Currently 3 is the highest' )

    parser.add_argument(
        '-c', '--recreate-index', action='store_true', default = False,
        help = 'if specified, pre-existing .index files will be deleted and newly created' )

    parser.add_argument(
        '-r', '--recursive', action='store_true', default = False,
        help = 'mount TAR archives inside the mounted TAR recursively. Note that this only has an effect when creating an index. If an index already exists, then this option will be effectively ignored. Recreate the index if you want change the recursive mounting policy anyways.' )

    parser.add_argument(
        '-s', '--serialization-backend', type = str, default = 'custom',
        help =
        'specify which library to use for writing out the TAR index. Supported keywords: (' +
        ','.join( IndexedTar.availableSerializationBackends ) + ')[.(' +
        ','.join( IndexedTar.availableCompressions ).strip( ',' ) + ')]' )

    parser.add_argument(
        '-p', '--prefix', type = str, default = '',
        help = 'The specified path to the folder inside the TAR will be mounted to root. '
               'This can be useful when the archive as created with absolute paths. '
               'E.g., for an archive created with `tar -P cf /var/log/apt/history.log`, '
               '-p /var/log/apt/ can be specified so that the mount target directory '
               '>directly< contains history.log.' )

    parser.add_argument(
        'tarfilepath', metavar = 'tar-file-path',
        type = argparse.FileType( 'r' ), nargs = 1,
        help = 'the path to the TAR archive to be mounted' )
    parser.add_argument(
        'mountpath', metavar = 'mount-path', nargs = '?',
        help = 'the path to a folder to mount the TAR contents into' )

    args = parser.parse_args()

    tarToMount = os.path.abspath( args.tarfilepath[0].name )
    try:
        tarfile.open( tarToMount, mode = 'r:' )
    except tarfile.ReadError:
        print( "Archive", tarToMount, "can't be opened!",
               "This might happen for compressed TAR archives, which currently is not supported." )
        exit( 1 )

    mountPath = args.mountpath
    if mountPath is None:
        mountPath = os.path.splitext( tarToMount )[0]

    mountPathWasCreated = False
    if not os.path.exists( mountPath ):
        os.mkdir( mountPath )

    printDebug = args.debug

    fuseOperationsObject = TarMount(
        pathToMount = tarToMount,
        clearIndexCache = args.recreate_index,
        recursive = args.recursive,
        serializationBackend = args.serialization_backend,
        prefix = args.prefix )

    fuse.FUSE( operations = fuseOperationsObject,
               mountpoint = mountPath,
               foreground = args.foreground )

    if mountPathWasCreated and args.foreground:
        os.rmdir( mountPath )

if __name__ == '__main__':
    cli()
