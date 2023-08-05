"""
================
Meta Information
================

This provides the meta and editorial information pertaining to the project.

Version Information
===================

:pep:`0440` prescribes the structure of versioning information in a standard Python package.

Maintainer Information
======================

This identifies the person who maintains the project and is probably the most pertinent information as it ensures its longevity.

Editorial Information
=====================

This acknowledges the contributions of the original author and subsequent contributors to the project.

Organization Information
========================

This identifies the entities supporting the project.
"""
# TODO : Merge with the __meta__ from paython/template

__project__ = "Web-Templates"                                       #: The project title
__summary__ = "Standardized templates for Python's web frameworks"  #: A summary of the project, used as the packages short description.

__company__ = 'Manaikan'                                    #: The company or organization name
__website__ = 'https://gitlab.com/manaikan/web-templates/'  #: The package or project home page; alternatively the company/organization or authors website.

__author__  = 'Carel van Dam'        #: The Package authors name
__e_mail__  = 'carelvdam@gmail.com'  #: The package authors e-mail address

__dialect__ = None              #: The version dialect or epoch indicates the
__release__ = (0,0,0)           #: The release number, major.minor.micro, serves as the package version number in :file:`setup.py`
__version__ = __release__[:-1]  #: The version number, major.minor, used predominantly within documentation
__entrant__ = ("Alpha", 0)      #: The release candidate, product status or entrant, aX|bX|rcX for alpha|beta|release candidate respectively.
__develop__ = None              #: The development revision, .devX, for minor bug fixes but no API changes.
__postnum__ = 2                 #: The post revision, .postX, for quick pushes where files and the like were accidentally excluded

__version__ = ".".join([str(item) for item in __version__]) # The effective version number for comparative purposes
__release__ = "{}!".format(__dialect__) if __dialect__ is not None else "" \
            + ".".join([str(item) for item in __release__]) \
            + {None    : lambda value : "".format(value)     if value is not None else "",
               "Alpha" : lambda value : "a{}".format(value)  if value is not None else "",
               "Beta"  : lambda value : "b{}".format(value)  if value is not None else "",
               "RC"    : lambda value : "rc{}".format(value) if value is not None else "",}[__entrant__[0]](__entrant__[1]) \
            + (".post{}".format(__postnum__) if __postnum__ is not None else "") \
            + (".dev{}".format(__develop__)  if __develop__ is not None else "") # The effective release number conforming to the mask [N!]N(.N)*[{a|b|rc}N][.postN][.devN]


