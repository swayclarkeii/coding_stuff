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

  // Load batch update JSON
  const updateData = JSON.parse(
    fs.readFileSync('/Users/swayclarke/coding_stuff/ambush-tv-presentation-update.json', 'utf8')
  );

  // Authenticate with OAuth
  const oauth2Client = new google.auth.OAuth2(client_id, client_secret);
  oauth2Client.setCredentials({
    refresh_token: tokens.refresh_token,
    access_token: tokens.access_token,
    expiry_date: tokens.expiry_date
  });

  const slides = google.slides({ version: 'v1', auth: oauth2Client });

  // Apply batch update
  console.log('Applying batch update to presentation:', updateData.presentationId);
  console.log('Number of requests:', updateData.requests.length);

  const response = await slides.presentations.batchUpdate({
    presentationId: updateData.presentationId,
    requestBody: {
      requests: updateData.requests
    }
  });

  console.log('✅ Batch update applied successfully!');
  console.log('Replies:', response.data.replies?.length || 0);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
