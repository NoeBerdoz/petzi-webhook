import hmac
import hashlib

from persistence.database import Database

class PetziAuthenticator:

    def __init__(self):
        self.shared_petzi_secret = None

    def get_shared_secret(self):
        if self.shared_petzi_secret is None:
            with Database.get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Get secret
                    cur.execute(
                        """
                           SELECT value FROM web_config WHERE name = 'shared_petzi_secret';
                       """)
                    result = cur.fetchone()
                    self.shared_petzi_secret = result[0] if result else None


    def verify_signature(self, request):
        if self.shared_petzi_secret is None: # I'm rushing
            self.get_shared_secret()

        """ Verify the Petzi-Signature header. """
        signature_header = request.headers.get('Petzi-Signature')
        if not signature_header:
            return False

        # Extract timestamp and signature from header
        parts = signature_header.split(',')
        if len(parts) != 2:
            return False

        timestamp_part = parts[0].strip()
        signature_part = parts[1].strip()

        if not timestamp_part.startswith('t=') or not signature_part.startswith('v1='):
            return False

        timestamp = timestamp_part[2:]
        signature = signature_part[3:]

        # Recompute the signature
        body = request.get_data(as_text=True)
        body_to_sign = f'{timestamp}.{body}'.encode()
        computed_signature = hmac.new(self.shared_petzi_secret.encode(), body_to_sign, hashlib.sha256).hexdigest()

        # Compare the signatures
        return hmac.compare_digest(computed_signature, signature)