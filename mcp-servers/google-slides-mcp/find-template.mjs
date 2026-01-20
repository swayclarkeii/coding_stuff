import { google } from 'googleapis';
import fs from 'fs';

async function main() {
  // Load OAuth credentials from gcp-oauth.keys.json
  const keysFile = JSON.parse(
    fs.readFileSync('/Users/swayclarke/coding_stuff/.credentials/gcp-oauth.keys.json', 'utf8')
  );
  const { client_id, client_secret } = keysFile.installed;

  // Load refresh token from google-drive-mcp tokens
  const tokens = JSON.parse(
    fs.readFileSync('/Users/swayclarke/.config/google-drive-mcp/tokens.json', 'utf8')
  );

  // Authenticate with OAuth
  const oauth2Client = new google.auth.OAuth2(client_id, client_secret);
  oauth2Client.setCredentials({
    refresh_token: tokens.refresh_token,
    access_token: tokens.access_token,
    expiry_date: tokens.expiry_date
  });

  const drive = google.drive({ version: 'v3', auth: oauth2Client });

  // Search for Proposal Template presentation
  console.log('Searching for Proposal Template...');
  const response = await drive.files.list({
    q: "name = 'Proposal Template' and mimeType = 'application/vnd.google-apps.presentation'",
    fields: 'files(id, name, parents)',
    spaces: 'drive'
  });

  if (response.data.files && response.data.files.length > 0) {
    response.data.files.forEach(file => {
      console.log(`Found: ${file.name}`);
      console.log(`  ID: ${file.id}`);
      console.log(`  Parents: ${file.parents ? file.parents.join(', ') : 'None'}`);
    });
  } else {
    console.log('No files found');
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
