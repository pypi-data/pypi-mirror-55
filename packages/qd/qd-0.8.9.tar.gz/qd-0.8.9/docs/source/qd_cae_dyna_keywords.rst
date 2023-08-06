

Keyword Types
-------------

The basic idea of these classes is, that the file should look identical if written again, except for modifications. Also comments shall be preserved. Please beware in case of parsing the mesh, since the rewritten floating point numbers will deviate in due to the machine precision. To prevent this deviation, just don't parse the mesh.

 - `KeyFile Introduction Article <http://www.qd-eng.de/index.php/2018/02/19/manipulating-ls-dyna-keyfiles-in-python/>`_

**Keyword**

    The generic ``Keyword`` class is used for all unknown keywords. If the mesh of a ``KeyFile`` is not parsed, then also the mesh keywords are seen as generic keywords. To read all keywords of a ``KeyFile`` use the ``read_keywords`` option.

    If a ``KeyFile`` is written again, it will look identical, since the class saves everything including the comments.
    
    .. toctree::
        :maxdepth: 3

        qd_cae_dyna_keywords_Keyword

    Ressources:
       - `Youtube Tutorial <https://youtu.be/wdOIw2m_YLk>`_
            
    Example:
    ::

        from qd.cae.dyna import *
        # open a file (without mesh parsing)
        kf = KeyFile("path/to/keyfile")
        # get the third part keyword
        generic_keyword = kf["*PART"][2]
        # set a new pid (searches pid in comment line above card)
        generic_keyword["pid"] = 100
        # save it
        kf.save("path/to/new_keyfile")

**Include Keywords**

    The specific include keyword classes provide means to deal with include files.
    Includes are loaded automatically, if in the ``KeyFile`` contructor argument ``load_includes=True``. The ``IncludePathKeyword`` manages all locations, where include files could be located, while the ``IncludeKeyword`` is resposible for managing the files. 

    .. toctree::
        :maxdepth: 3

        qd_cae_dyna_keywords_IncludeKeyword
        qd_cae_dyna_keywords_IncludePathKeyword

    Ressources:
       - `Youtube Tutorial <https://youtu.be/ZGiyNSxr4Eg>`_
    
        
    Example:
    ::

        from qd.cae.dyna import *
        # open a file
        kf = KeyFile("path/to/keyfile", load_includes=True)
        # get first include keyword
        include_keyword = kf["*INCLUDE"][0]
        # get the include(s) of the keyword
        includes = include_keyword.get_includes()
        # or get all loaded includes at once 
        includes = kf.get_includes()

    .. note::
        All the keywords of the includes are not accessible from the main ``KeyFile``, but only from the include ``KeyFile``, which can be retrieved by ``KeyFile.get_includes``.

**Mesh Keywords**
    
    The mesh pecific Keywords:

    .. toctree::
        :maxdepth: 3

        qd_cae_dyna_keywords_NodeKeyword
        qd_cae_dyna_keywords_ElementKeyword
        qd_cae_dyna_keywords_PartKeyword

    are only created, if opening a ``KeyFile`` with the argument ``parse_mesh`` enabled. If the mesh is not parsed, their data is seen as a generic ``Keyword``.
    
    Ressources:
       - `Youtube Tutorial <https://youtu.be/CkelV3MI6Jg>`_


    Example
    ::

        from qd.cae.dyna import *
        # load a file
        kf = KeyFile("path/to/keyfile", 
                      parse_mesh=True, 
                      load_includes=True)
        # get first node keyword
        node_keyword = kf["*NODE"][0]
        # add a node
        node_keyword.add_node(6728, x=1, y=2, z=3)
        # and save again
        kf.save("path/to/new_keyfile")

    .. warning::
        If parsing the mesh, all keywords except for the ``PartKeyword`` stop parsing if they encounter a comment or empty line in the data block (e.g. between two elements or nodes)

    .. warning::
        Mesh entities, such as nodes can be created, but not deleted. Also the mesh keywords itself can not be deleted.



