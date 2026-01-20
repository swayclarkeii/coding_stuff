import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Load OAuth credentials
const keysPath = path.join(__dirname, 'dist', 'gcp-oauth.keys.json');
const keys = JSON.parse(fs.readFileSync(keysPath, 'utf-8'));

const oauth2Client = new google.auth.OAuth2(
  keys.installed.client_id,
  keys.installed.client_secret,
  keys.installed.redirect_uris[0]
);

// Authorization code from OAuth flow
const authCode = '4/0ASc3gC1DGH7S6Mef9e3jaHh3XLXqsY35n9PCxtyesHuvgelryvh7iOpDz9fSRcd3J8obAw';

// Exchange code for tokens
try {
  const { tokens } = await oauth2Client.getToken(authCode);
  console.log('✅ Tokens received successfully!');
  console.log(JSON.stringify(tokens, null, 2));

  // Save tokens to file
  const tokenPath = path.join(__dirname, 'dist', 'gcp-oauth.token.json');
  fs.writeFileSync(tokenPath, JSON.stringify(tokens, null, 2));
  console.log(`\n✅ Tokens saved to: ${tokenPath}`);
} catch (error) {
  console.error('❌ Error exchanging code for tokens:');
  console.error(error.message);
  process.exit(1);
}
