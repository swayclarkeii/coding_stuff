const data = $input.first().json;
const score = data.sop_score || 0;
const name = data.name || 'there';
const previousScore = data.previous_score || null;
const submissionCount = data.submission_count || 1;

const elementMap = {
  purpose: { name: 'Purpose Statement', why: 'No clear statement of why this procedure exists.', fix: 'Add a Purpose section explaining why this process matters.' },
  preparation: { name: 'Preparation Section', why: 'Team may start unprepared without prerequisites listed.', fix: 'Add a Preparation section with tools, training, and prerequisites.' },
  process: { name: 'Process Flow', why: 'Numbered steps with decision points ensure consistency.', fix: 'Break down into numbered steps using action verbs.' },
  checklist: { name: 'Checklist/Verification', why: 'Cannot confirm process was followed correctly.', fix: 'Add a checklist with key verification points.' },
  document: { name: 'Document Control', why: 'Without version tracking, SOPs become outdated.', fix: 'Add version number, author, review date.' }
};

function getElementDetails(element) {
  const el = (element || '').toLowerCase();
  const keys = Object.keys(elementMap);
  for (var i = 0; i < keys.length; i++) {
    if (el.includes(keys[i])) { var result = elementMap[keys[i]]; return result; }
  }
  var fallback = { name: element, why: 'This element is missing.', fix: 'Review the 5 core SOP elements.' };
  return fallback;
}

const quickWins = data.top_3_quick_wins || [];
var quickWinsHtml = '';
for (var qi = 0; qi < quickWins.length; qi++) {
  var w = quickWins[qi];
  quickWinsHtml += '<div style="display:flex;margin:12px 0;padding:12px;background:#2a2a2a;border-radius:6px;"><div style="font-size:24px;font-weight:bold;color:#d4af37;margin-right:15px;">' + (qi+1) + '</div><div><strong>' + (w.title||'Quick Win') + '</strong><p style="margin:4px 0 0;color:#ccc;">' + (w.action||'Action needed') + '</p></div></div>';
}
if (!quickWinsHtml) { quickWinsHtml = '<p>Quick wins will be provided.</p>'; }

var progressBadge = '';
if (submissionCount > 1 && previousScore !== null) {
  progressBadge = '<div style="text-align:center;margin:20px 0;padding:15px;background:#1a1a1a;border-radius:8px;"><span style="color:#999;">Previous:</span> <span style="font-size:24px;color:#999;">' + previousScore + '%</span> <span style="color:#d4af37;font-size:24px;margin:0 10px;">\u2192</span> <span style="color:#d4af37;">Now:</span> <span style="font-size:24px;color:#F26B5D;">' + score + '%</span></div>';
}

const missingElements = data.missing_elements || [];
var missingHtml = '';
for (var mi = 0; mi < missingElements.length; mi++) {
  var el = missingElements[mi];
  var d = (typeof el === 'object' && el !== null) ? { name: el.element_name || 'Unknown', why: el.why_it_matters || 'Missing.', fix: el.how_to_fix || 'Review SOP elements.' } : getElementDetails(el);
  missingHtml += '<div style="margin:15px 0;padding:15px;background:#2a2a2a;border-radius:6px;"><strong style="color:#F26B5D;">\u2610 ' + d.name + '</strong><p style="color:#ccc;margin:5px 0;"><em>Why:</em> ' + d.why + '</p><p style="color:#E8A317;margin:5px 0;"><em>Fix:</em> ' + d.fix + '</p></div>';
}
if (!missingHtml) { missingHtml = '<p>Analysis not available</p>'; }

// Updated resubmit URL with score and quick wins encoded
var resubmitUrl = 'https://sopbuilder.oloxa.ai?lead=' + (data.lead_id||'') + '&email=' + encodeURIComponent(data.email||'') + '&name=' + encodeURIComponent(name) + '&score=' + score + '&wins=' + encodeURIComponent(JSON.stringify(quickWins));

var html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <style>body{font-family:Arial,sans-serif;background:#000;color:#fff;margin:0;padding:0}</style>
</head>
<body>
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;">
    <!-- Updated logo section -->
    <div style="text-align:center;margin-bottom:40px;">
      <img src="https://sopbuilder.oloxa.ai/logo.png" alt="OLOXA" style="height:40px;width:180px;">
    </div>

    <h1 style="color:#fff;font-size:28px;text-align:center;">Hey ${name}, here's your SOP analysis.</h1>

    ${progressBadge}

    <div style="font-size:64px;font-weight:bold;color:#F26B5D;text-align:center;margin:30px 0;">${score}%</div>
    <p style="text-align:center;font-size:18px;color:#fff;margin:10px 0;">Your SOP Completeness Score</p>
    <p style="text-align:center;font-size:16px;color:#ccc;font-style:italic;margin-bottom:30px;">Great start! With a few improvements, you'll be on your way.</p>

    <div style="margin:30px 0;padding:25px;background:#1a1a1a;border-left:4px solid #F26B5D;border-radius:4px;">
      <h2 style="color:#F26B5D;font-size:20px;margin-top:0;">Your Goal</h2>
      <p><strong style="color:#F26B5D;">Intention:</strong> ${data.goal||'Not specified'}</p>
      <p><strong style="color:#F26B5D;">Department:</strong> ${data.department||'General'}</p>
      <p><strong style="color:#F26B5D;">Who will use this:</strong> ${data.end_user||'Not specified'}</p>
    </div>

    <div style="margin:30px 0;padding:25px;background:#1a1a1a;border-left:4px solid #F26B5D;border-radius:4px;">
      <h2 style="color:#F26B5D;font-size:20px;margin-top:0;">What's Missing</h2>
      <p style="font-size:13px;color:#999;">Based on the 5 core elements every SOP needs:</p>
      ${missingHtml}
    </div>

    <div style="margin:30px 0;padding:25px;background:#1a1a1a;border-left:4px solid #F26B5D;border-radius:4px;">
      <h2 style="color:#F26B5D;font-size:20px;margin-top:0;">3 Quick Wins to Improve Your Score</h2>
      ${quickWinsHtml}
      <div style="background:#2a2a2a;border-left:4px solid #d4af37;padding:15px;margin:15px 0;border-radius:4px;font-size:14px;">
        <strong>Note:</strong> This is a starting point — resubmit with improvements to raise your score.
      </div>
    </div>

    <div style="background:linear-gradient(135deg,#F26B5D,#ff8577);padding:30px;text-align:center;margin:40px 0;border-radius:10px;">
      <p style="color:#000;font-size:18px;font-weight:bold;">Ready to improve your score?</p>
      <a href="${resubmitUrl}" style="display:inline-block;background:#d4af37;color:#000;text-decoration:none;font-weight:bold;font-size:18px;padding:15px 35px;border-radius:10px;">Resubmit Your Improved SOP</a>
    </div>

    <div style="text-align:center;color:#3B3B3B;font-size:12px;margin-top:40px;">© 2026 OLOXA.AI</div>
  </div>
</body>
</html>`;

var output = { ...data, html_report: html, email_subject: 'Your SOP Analysis - Score: ' + score + '%' };
return [{ json: output }];
