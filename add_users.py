import requests
import sys
import re

accessKey = ''

def main():
    # Get the access key
    global accessKey

    if len(sys.argv) < 4:
        print "\nUse this script to add all users from an organisation into an organisational team."
        print "Usage: ./" + sys.argv[0] + " access_key organisation organisation_team\n"
        quit()
    else:
        accessKey = sys.argv[1]
        organisation = sys.argv[2]
        team = sys.argv[3].lower()
        team_id = -1

    # Get and check the team
    teams = github_api_get_request("orgs/"+organisation+"/teams")
    for t in teams:
        if t['slug'].lower() == team:
            team_id = t['id']
            continue

    if team_id == -1:
        print "ERROR: Could not find team within Organisation."
        exit()
    else:
        print "Team-ID: " + str(team_id)

    # Get the users
    print "Processing users..."
    users = github_api_get_request("orgs/"+organisation+"/members")
    for user in users:
        # For each user, add to team
        # https://developer.github.com/v3/orgs/teams/#add-team-membership
        # PUT /teams/:id/memberships/:username
        print "Processing: " + user['login']
        x = github_api_put_request("teams/" + str(team_id) + "/memberships/" + user['login'])
        print "\t User is an " + x['state'] + " " + x['role']


def github_api_get_request(path):

    r = requests.get("https://api.github.com/" + path, auth=(accessKey, ''))
    if r.status_code != 200:
        print "ERROR: Request to " + path + " resulted with " + str(r.status_code)
        print "ERROR: Check all your parameters."
        quit()

    buf = r.json()

    if 'link' in r.headers:
        m = re.search('https://api.github.com/([\w/?=&]+)>; rel="next"', r.headers['link'])
        if m:
            resp = github_api_get_request(m.group(1))
            for a in resp:
                buf.append(a)

    return buf

def github_api_put_request(path):
    r = requests.put("https://api.github.com/" + path, auth=(accessKey, ''))

    if r.status_code != 200:
        print "ERROR: Request to " + path + " resulted with " + str(r.status_code)
        print "ERROR: Internal error when updating team membership."
        quit()

    return r.json()

# Here's our payoff idiom!
if __name__ == '__main__':
    main()