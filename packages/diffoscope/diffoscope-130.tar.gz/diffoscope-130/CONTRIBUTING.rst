Contributing
============

The preferred way to report bugs about diffoscope, as well as suggest fixes and
requests for improvements, is to submit reports to the issue tracker at
https://salsa.debian.org/reproducible-builds/diffoscope/issues

You can also submit patches via *merge request* to Salsa, Debian's Gitlab. Start
by forking the `diffoscope Git
repository <https://salsa.debian.org/reproducible-builds/diffoscope>`__
(see
`documentation <https://salsa.debian.org/help/gitlab-basics/fork-project.md>`__),
make your changes and commit them as you normally would. You can then push your
changes and submit a *merge request* via Salsa.  See `Gitlab documentation
<https://salsa.debian.org/help/gitlab-basics/add-merge-request.md>`__ about
*merge requests*.

You can also submit bugs about Debian specific issues to the Debian bug tracker. 


Add a comparator
================

Diffoscope doesn't support a specific file type? Please contribute to the
project! Each file type is handled by a comparator, and writing a new one is
usually very easy.
Here are the steps to add a new comparator:

- Add the new comparator in ``diffoscope/comparators/`` (have a look at the
  other comparators in the same directory to have an idea of what to do)
- Declare the comparator File class in ``ComparatorManager`` in
  ``diffoscope/comparators/__init__.py``
- Add a test in ``tests/comparators/``
- If required, update the ``Build-Depends`` list in ``debian/control``
- If required, update the ``EXTERNAL_TOOLS`` list in
  ``diffoscope/external_tools.py``

Uploading the package
=====================

When uploading diffoscope to the Debian archive, please take extra care to make
sure the uploaded source package is correct, that is it includes the files
tests/data/test(1|2).(a|o) which in some cases are removed by dpkg-dev when
building the package. See `#834315 <https://bugs.debian.org/834315>`__ for an example
FTBFS bug caused by this. (See `#735377
<https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=735377#44>`__ and followups
to learn how this happened and how to prevent it)

Please also release a signed tarball::

    $ VERSION=FIXME
    $ git archive --format=tar --prefix=diffoscope-${VERSION}/ ${VERSION} | bzip2 -9 > diffoscope-${VERSION}.tar.bz2
    $ gpg --detach-sig --armor --output=diffoscope-${VERSION}.tar.bz2.asc < diffoscope-${VERSION}.tar.bz2

And commit them to our LFS repository at https://salsa.debian.org/reproducible-builds/reproducible-lfs

After uploading, please also update the version on PyPI using::

   $ python3 setup.py sdist upload --sign

Once the tracker.debian.org entry appears, consider tweeting the release on
``#reproducible-builds`` with::

  %twitter diffoscope $VERSION has been released. Check out the changelog here: $URL

Finally, update the Docker image using::

    docker build -t registry.salsa.debian.org/reproducible-builds/diffoscope .
    docker push registry.salsa.debian.org/reproducible-builds/diffoscope
