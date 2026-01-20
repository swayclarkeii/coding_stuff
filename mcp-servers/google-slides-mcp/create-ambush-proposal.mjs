import { google } from 'googleapis';
import fs from 'fs';

async function main() {
  // Load OAuth credentials
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
  const slides = google.slides({ version: 'v1', auth: oauth2Client });

  const TEMPLATE_ID = '17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ';
  const NEW_NAME = 'Ambush TV - Proposal (Back Pocket) - Jan 2026';

  // Step 1: Duplicate the template
  console.log('Duplicating Proposal Template...');
  const copyResponse = await drive.files.copy({
    fileId: TEMPLATE_ID,
    requestBody: {
      name: NEW_NAME
    }
  });

  const newPresentationId = copyResponse.data.id;
  console.log(`✅ Created new presentation: ${NEW_NAME}`);
  console.log(`   ID: ${newPresentationId}`);

  // Step 2: Create batch update with proposal variables
  const requests = [
    // SLIDE 1: TITLE
    { replaceAllText: { containsText: { text: '{{company_name}}', matchCase: false }, replaceText: 'Ambush TV' }},
    { replaceAllText: { containsText: { text: '{{date}}', matchCase: false }, replaceText: 'January 2026' }},

    // SLIDE 2: CLIENT CONTEXT
    { replaceAllText: { containsText: { text: '{{client_company_description}}', matchCase: false }, replaceText: 'Ambush TV creates advertising pitch presentations for commercial directors, managing 50+ projects monthly with a team of 9 core people and 70-80 freelancers.' }},
    { replaceAllText: { containsText: { text: '{{client_name}}', matchCase: false }, replaceText: 'Sindbad & Pierre' }},

    // SLIDE 3: OPPORTUNITIES (PAIN POINTS)
    { replaceAllText: { containsText: { text: '{{pain_point_1}}', matchCase: false }, replaceText: '€150K in Outstanding Client Payments' }},
    { replaceAllText: { containsText: { text: '{{pain_point_1_description}}', matchCase: false }, replaceText: '€100,000 overdue by more than 30 days. Late invoicing and no systematic follow-up delays collection. Direct cost of capital: €5,000/year.' }},
    { replaceAllText: { containsText: { text: '{{pain_point_2}}', matchCase: false }, replaceText: 'Data Silos Creating 5+ Hours/Week of Manual Work' }},
    { replaceAllText: { containsText: { text: '{{pain_point_2_description}}', matchCase: false }, replaceText: '12+ sheets that don\'t sync. Names don\'t match, team changes require manual updates everywhere, rates require triple-entry. Admin team buried in data transfer.' }},
    { replaceAllText: { containsText: { text: '{{pain_point_3}}', matchCase: false }, replaceText: '22 Hours/Month on Invoice Validation' }},
    { replaceAllText: { containsText: { text: '{{pain_point_3_description}}', matchCase: false }, replaceText: 'Sindbad manually validates 15-25 invoices weekly, catching 10% error rate. Each error costs €150 average to investigate and correct.' }},

    // SLIDE 4: SOLUTIONS
    { replaceAllText: { containsText: { text: '{{product_benefit_1}}', matchCase: false }, replaceText: 'Single Source of Truth Architecture' }},
    { replaceAllText: { containsText: { text: '{{product_benefit_1_description}}', matchCase: false }, replaceText: 'Data entered once, flows everywhere. Calendar to Dashboard to Project Directory. Names normalized. Team changes reflect automatically.' }},
    { replaceAllText: { containsText: { text: '{{product_benefit_2}}', matchCase: false }, replaceText: 'Systematic Collection & Visibility' }},
    { replaceAllText: { containsText: { text: '{{product_benefit_2_description}}', matchCase: false }, replaceText: 'Calendar-driven reminders for hours collection and invoicing. Aging dashboard shows who owes what. Freed admin capacity to chase overdue payments.' }},
    { replaceAllText: { containsText: { text: '{{product_benefit_3}}', matchCase: false }, replaceText: 'Invoice Pre-Validation with Human Checkpoints' }},
    { replaceAllText: { containsText: { text: '{{product_benefit_3_description}}', matchCase: false }, replaceText: 'Automated extraction and validation. Exceptions flagged for Sindbad\'s review. Reduces validation time 50-80% while keeping human judgment.' }},

    // SLIDE 5: TIMELINE
    { replaceAllText: { containsText: { text: '{{building_phase_time}}', matchCase: false }, replaceText: '4-6 weeks' }},
    { replaceAllText: { containsText: { text: '{{building_phase_description}}', matchCase: false }, replaceText: 'Phase 1: Quick Wins - Rate sync, calendar reminders, Fathom integration, dashboard validation rules.' }},
    { replaceAllText: { containsText: { text: '{{deployment_phase_time}}', matchCase: false }, replaceText: '8-10 weeks' }},
    { replaceAllText: { containsText: { text: '{{deployment_phase_description}}', matchCase: false }, replaceText: 'Phase 2: Invoice Validation - Invoice parsing, cross-reference checks, exception dashboard, Wise payment preparation.' }},
    { replaceAllText: { containsText: { text: '{{testing_phase_time}}', matchCase: false }, replaceText: '2-4 weeks' }},
    { replaceAllText: { containsText: { text: '{{testing_phase_description}}', matchCase: false }, replaceText: 'Training, documentation, parallel run with manual process, gradual handoff.' }},

    // SLIDE 6: WHAT TO EXPECT
    { replaceAllText: { containsText: { text: '{{Client_expectations_list}}', matchCase: false }, replaceText: '• Access to Google Sheets and relevant documentation\n• 2-3 hours/week for feedback during build\n• Participation in training sessions\n• Champion from admin team for testing' }},
    { replaceAllText: { containsText: { text: '{{Client_Name}}', matchCase: false }, replaceText: 'Ambush TV' }},
    { replaceAllText: { containsText: { text: '{{oloxa_delivery_list}}', matchCase: false }, replaceText: '• Production-ready automations\n• Admin team training (1-2 sessions)\n• Full documentation package\n• 30-60 days post-launch support\n• Weekly progress updates during build' }},

    // SLIDE 7: METRICS AND Q&A
    { replaceAllText: { containsText: { text: '{{metric_1_title}}', matchCase: false }, replaceText: 'Time Savings' }},
    { replaceAllText: { containsText: { text: '{{metric_1_description}}', matchCase: false }, replaceText: '20+ hours/month returned to high-value work' }},
    { replaceAllText: { containsText: { text: '{{metric_2_title}}', matchCase: false }, replaceText: 'Error Prevention' }},
    { replaceAllText: { containsText: { text: '{{metric_2_description}}', matchCase: false }, replaceText: '€9,000/year in avoided error costs' }},
    { replaceAllText: { containsText: { text: '{{metric_additional_title}}', matchCase: false }, replaceText: 'Cash Flow Improvement' }},
    { replaceAllText: { containsText: { text: '{{metric_additional_description}}', matchCase: false }, replaceText: '€150K outstanding tracked, faster collection' }},
    { replaceAllText: { containsText: { text: '{{question_1}}', matchCase: false }, replaceText: 'What if it doesn\'t work?' }},
    { replaceAllText: { containsText: { text: '{{answer_1}}', matchCase: false }, replaceText: 'Phase 1 is low-risk (4-6 weeks, proven patterns). No obligation for Phase 2 until Phase 1 proves value.' }},
    { replaceAllText: { containsText: { text: '{{question_2}}', matchCase: false }, replaceText: 'Can we start smaller?' }},
    { replaceAllText: { containsText: { text: '{{answer_2}}', matchCase: false }, replaceText: 'Yes - €8K minimum viable package proves concept first. Upgrade to full solution once value is demonstrated.' }},
    { replaceAllText: { containsText: { text: '{{question_3}}', matchCase: false }, replaceText: 'What about ongoing support?' }},
    { replaceAllText: { containsText: { text: '{{answer_3}}', matchCase: false }, replaceText: '30 days included. Extended support available at €1,500/quarter for priority bug fixes and minor enhancements.' }},
    { replaceAllText: { containsText: { text: '{{question_4}}', matchCase: false }, replaceText: 'How does this work with our free tools?' }},
    { replaceAllText: { containsText: { text: '{{answer_4}}', matchCase: false }, replaceText: 'Built specifically for Google Sheets, Discord, Gmail. No enterprise licenses needed. API-based integration works with free tools.' }},

    // SLIDE 8: INVESTMENT
    { replaceAllText: { containsText: { text: '{{time_based_cost}}', matchCase: false }, replaceText: '€20,000-22,500' }},
    { replaceAllText: { containsText: { text: '{{value_based_cost}}', matchCase: false }, replaceText: '€28,400/year' }},
    { replaceAllText: { containsText: { text: '{{value_based_description}}', matchCase: false }, replaceText: 'Total annual value: €28,400 (Sindbad time: €13,200 + Admin time: €1,200 + Error prevention: €9,000 + Cash flow: €5,000). Payback: 8-10 months.' }},
    { replaceAllText: { containsText: { text: '{{client_investment_1}}', matchCase: false }, replaceText: 'Phase 1: Quick Wins - €6,500\n(Rate sync, calendar reminders, Fathom, validation rules)\nTimeline: 4-6 weeks | Payback: 2-4 months' }},
    { replaceAllText: { containsText: { text: '{{client_investment_2}}', matchCase: false }, replaceText: 'Phase 2: Invoice Validation - €16,000\n(Invoice parsing, cross-reference, exception dashboard, Wise prep)\nTimeline: 8-10 weeks | Payback: 8-12 months\n\nCombined: €20,000 (11% discount)' }},
    { replaceAllText: { containsText: { text: '{{minimum_viable_package}}', matchCase: false }, replaceText: '€8,000 - Core Automation Bundle\n• Rate synchronization system\n• Invoice pre-validation helper (50% time reduction)\n• Fathom integration\nTimeline: 4-5 weeks | Payback: 8 months' }},

    // SLIDE 9: NEXT STEPS
    { replaceAllText: { containsText: { text: '{{step_1_description}}', matchCase: false }, replaceText: 'Decide which package fits your budget and priorities\n(Minimum Viable €8K | Phase 1 €6.5K | Full Solution €20K)' }},
    { replaceAllText: { containsText: { text: '{{step_2_description}}', matchCase: false }, replaceText: 'Schedule kickoff call with admin team for requirements confirmation' }},
    { replaceAllText: { containsText: { text: '{{step_3_description}}', matchCase: false }, replaceText: 'Begin Phase 1 development (start within 1 week of agreement)' }},

    // SLIDE 10: THANK YOU
    { replaceAllText: { containsText: { text: '{{unique_client_thank_you_message}}', matchCase: false }, replaceText: 'Ambush has built something impressive - €150K in monthly freelancer payments, 50+ projects, and a reputation for excellence. Looking forward to helping it run even smoother.' }}
  ];

  // Step 3: Apply batch update
  console.log(`\nApplying ${requests.length} text replacements...`);
  const updateResponse = await slides.presentations.batchUpdate({
    presentationId: newPresentationId,
    requestBody: { requests }
  });

  console.log(`✅ Batch update applied successfully!`);
  console.log(`   Replacements: ${updateResponse.data.replies?.length || 0}`);
  console.log(`\n📎 Presentation URL: https://docs.google.com/presentation/d/${newPresentationId}/edit`);
}

main().catch(err => {
  console.error('Error:', err.message);
  if (err.response) {
    console.error('Details:', JSON.stringify(err.response.data, null, 2));
  }
  process.exit(1);
});
