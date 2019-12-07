======================
Exodus
======================

# License

This software is released under the [GPL 3.0 license] [1].
[1]: http://www.gnu.org/licenses/gpl-3.0.html

# Contribution

* Please follow the [PEP-8 Guidelines](https://www.python.org/dev/peps/pep-0008) when contributing new code or modifying
already existing one

# Forking

To make merge requests you need to fork this project, commit your changes and then create a Merge Request.

Any changes on the main repository will not be synced to your fork and you will have to do this manually.

To keep your fork up-to-date with the main project (upstream) follow these steps.

#### In your fork folder, add the uptream repository

```git remote add upstream https://<your_username>@dev.tvaddons.ag/tvaddons/plugin.video.exodus.git```

#### Checkout your local branch

```git checkout master```

#### Fetch the changes from upstream into its respective local branch (upstream/master)

```git fetch upstream```

#### Merge changes from upstream into your local branch

```git merge upstream/master```

#### Push your updated fork to the remote repository

```git push```

