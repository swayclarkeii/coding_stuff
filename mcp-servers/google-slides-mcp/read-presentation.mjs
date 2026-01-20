import { google } from 'googleapis';
import fs from 'fs';

async function main() {
  const keysFile = JSON.parse(
    fs.readFileSync('/Users/swayclarke/coding_stuff/.credentials/gcp-oauth.keys.json', 'utf8')
  );
  const { client_id, client_secret } = keysFile.installed;

  const tokens = JSON.parse(
    fs.readFileSync('/Users/swayclarke/.config/google-drive-mcp/tokens.json', 'utf8')
  );

  const oauth2Client = new google.auth.OAuth2(client_id, client_secret);
  oauth2Client.setCredentials({
    refresh_token: tokens.refresh_token,
    access_token: tokens.access_token,
    expiry_date: tokens.expiry_date
  });

  const slides = google.slides({ version: 'v1', auth: oauth2Client });

  const presentationId = process.argv[2] || '14vm54Yjro2IOQA5elxxnpIbQUu6xssiFKlfESaJZsdE';

  console.log(`Reading presentation: ${presentationId}\n`);

  const response = await slides.presentations.get({
    presentationId: presentationId
  });

  const presentation = response.data;
  console.log(`Title: ${presentation.title}\n`);
  console.log(`Total slides: ${presentation.slides.length}\n`);
  console.log('='.repeat(80));

  presentation.slides.forEach((slide, index) => {
    console.log(`\n--- SLIDE ${index + 1} ---`);

    if (slide.pageElements) {
      slide.pageElements.forEach(element => {
        if (element.shape && element.shape.text) {
          const textContent = element.shape.text.textElements
            ?.filter(te => te.textRun)
            .map(te => te.textRun.content)
            .join('')
            .trim();

          if (textContent) {
            console.log(`\n${textContent}`);
          }
        }
      });
    }
    console.log('\n' + '-'.repeat(40));
  });
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
