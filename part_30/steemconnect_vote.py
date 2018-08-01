from steemconnect.client import Client
from steemconnect.operations import Vote
from datetime import datetime

import database

CLIENT_ID = ''
CLIENT_SECRET = ''


# Fetch the access token for the voter from the database,
# verify that the access token is still valid, if not refresh.
# Perform the vote and check if the vote was performed correctly
# Log any errors.
def vote(self, voter, author, permlink, weight):
        db = database.Database()

        result = db.get_user_auth(voter)
        access_token, refresh_token, expire_on = result[0]
        dt = datetime.now()
        c = Client(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                access_token=access_token,
            )

        try:
            # Verify access_token
            if dt > expire_on:
                result = c.refresh_access_token(
                            refresh_token,
                            "login,vote"  # scopes
                )
                access_token = result['access_token']
                refresh_token = result['refresh_token']
                expires_in = result['expires_in']
                # Update access token in the DB
                self.db.update_authentication_tokens(
                    voter,
                    access_token,
                    refresh_token,
                    expires_in,
                    self.timestamp,
                )
                print('Updated access token\n')

            # Perform vote
            vote = Vote(voter, author, permlink, weight)
            result = c.broadcast([vote.to_operation_structure()])

            # Log vote
            if 'error' in result:
                message = result['error_description']
                db.add_to_error_log(
                    voter, author, permlink, weight,
                    message, self.timestamp,
                 )
            else:
                message = 'Succes'
                print(f"Voter: {voter}\nAuthor: {author}\n" +
                      f"Permlink: {permlink}\nWeight: {weight}\n" +
                      "Upvote succes\n")
        except Exception as error:
            db.add_to_error_log(
                voter, author, permlink,
                weight, error, self.timestamp,
            )
