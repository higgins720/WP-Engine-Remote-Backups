# WP Engine Remote Backup
Initiates a backup of a given site on WP Engine

## Goals

My vision for this is to be able to provide a list of environments by name, step through each one and:

1. Run a backup of the site, and wait until backup is completed before next step. 
2. Check for WP Core update if available, update if it is. 
3. Check for plugin updates, update all available. 
4. Check for theme update, update if it can. 
5. Check site status, 
6. If site gets 404 error, provide link and option to restore backup. 
7. Prompt user to continue to next site

This will probably change in the future, I'll probably want to modify things and add features down the road. For now I'd like to get this to work and make it easy for someone else to use on their machine without any reconfiguring.

## Features of the Future

### Store Private Data Locally
Write a hidden, encrypted file with api-key, as well as a seperate file of the list of sites with all the important information.

### Restore from Backup
There has to be a way to use the backup to restore the site, rather than going in manually to WPE engine and clicking "restore". I'll have to just figure that out.

### Schedule updates
For instance, schedule all sites to be done at 1am. This might be nice to have, if I can automatically run a site-restore after the program detects serious issues have occurred. That way you don't have to wake up the next day and find all the sites broken, or nothing was updated because it stopped after the first site had an issue.
