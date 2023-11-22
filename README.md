# ACL Bibliography Files for Overleaf

Overleaf supports uploading up to 50 MB per file, however currently the bib file [anthology.bib](http://aclweb.org/anthology/anthology.bib) exceeds 50 MB. Thus, to easily use the bib file on overleaf this repository provides split files each < 50 MB.

**TL;DR.** https://github.com/acl-org/acl-style-files/issues/25

Find the latest release below:

**Latest:** [anthology_bib.zip](https://github.com/devrimcavusoglu/acl-bib-overleaf/releases/download/231122/anthology_bib-231122.zip) 

Unzip the compressed archive of anthology bib files, and modify your `.tex` file to include all bibs.


```tex
\bibliography{anthology,anthology_p2,custom}  % add more bib files as required.
```


# License

The resource is licensed under MIT.   