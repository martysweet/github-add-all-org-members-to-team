Github Organisational Team Adder
================================

This script is a quick way to add all your organisations members into a single team.

The script uses an access key (which requires _org_ permissions) to call the following endpoints: 
* orgs/:org/teams (used to get the team unique ID)
* orgs/:org/members (used to get the organisation members)
* teams/:teamid/memberships/:username (used to add the user to the team)
 
The script can be run as follows:
> python add_users.py myverysecretpersonalaccesskey My-Organisation team-name
