# Team Notes #

## Link Issues and Change Revisions ##

Please use the following comment styles to create links between project issues and code and data change revisisions. svn does not enforce any of this automatically.

  * Please create an issue for one or more code & data commits. Do not commit changes without an associated issue.
  * When you commit a change, please prefix it with "[issue 87](https://code.google.com/p/emoji4unicode/issues/detail?id=87): ", where 87 is the actual issue number, as in `svn commit -m 'issue 87: blah describe your changes'`.
    * Later when we look at changes in the web UI, the "[issue 87](https://code.google.com/p/emoji4unicode/issues/detail?id=87)" is automatically turned into a link to that issue.
  * After committing a changeset, note the new revision number (for example, [revision 125](https://code.google.com/p/emoji4unicode/source/detail?r=125)) and add a comment to the issue referring back to that revision. In the comment, use "r" followed immediately by the revision number. For example, add a comment like "Implemented in [r125](https://code.google.com/p/emoji4unicode/source/detail?r=125)."
    * This is a great time to also change the issue status to "Fixed" if you are done.
    * Later when we look at [issue 87](https://code.google.com/p/emoji4unicode/issues/detail?id=87) in the web UI, the "[r125](https://code.google.com/p/emoji4unicode/source/detail?r=125)" is automatically turned into a link to that changeset.
  * It is good practice to have someone review changes. If a revision is good, mark it positive and move the issue Status to "Verified".

## Further Tips for Comments and Wiki Pages ##

In issue comments, you can refer to another issue with "[issue 87](https://code.google.com/p/emoji4unicode/issues/detail?id=87)" which will automatically be turned into a link to that issue.

You can refer to a revision (changeset) in both issue comments and wiki pages using the "r" prefix, as in [r125](https://code.google.com/p/emoji4unicode/source/detail?r=125), and have it be turned into a link.

# Changes on trunk vs. in a branch #

**Make "small" changes directly on the trunk.**
Please send another project member an email to review each change and issue, and add them to the issue's cc list. The reviewer should mark a change with a positive score and change the issue status from Fixed to Verified.

For changes that are "large", disruptive, controversial, or require several commits over more than a day, **please create a branch**, make one or more commits there, and get the whole branch reviewed by another member. Then merge the whole set back into the trunk. See the [SVN manual chapter about branching and merging](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.html).

Use your judgment for what's "large" or disruptive, or ask the team.

## Before you commit changes ##

Run tests and generate versioned data files:

```
cd src
./run_tests.sh
./gen_all.sh
```

Then check the diffs to make sure you are happy with the changes. For example: `svn diff --diff-cmd kdiff3`