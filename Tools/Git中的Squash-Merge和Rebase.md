# Git Squash, Merge, or Rebase?

![merge](./images/merge-squash-rebase.png)

## `merge`

![merge](./images/merge.png)

>
>Merge will create a merge commit that joins two branches together. With the fast-forward-only flag ff-only, git will attempt to merge without a merge commit, but this isn't possible if the branches have diverged (i.e., there has been a commit to the parent branch that's not on the feature branch).

## `--squash`
![merge](./images/merge-squash.png)

```
Squash commit -- not updating HEAD
Automatic merge failed; fix conflicts and then commit the result.
```

```
Squash commit -- not updating HEAD
Automatic merge went well; stopped before committing as requested

```
## `--rebase`
![merge](./images/rebase.png)

Line

[Squash, Merge, or Rebase? - Matt Rickard](https://matt-rickard.com/squash-merge-or-rebase)

[图解4种git合并分支方法](https://yanhaijing.com/git/2017/07/14/four-method-for-git-merge/)