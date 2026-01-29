const data = $input.first().json;
const score = data.sop_score || 0;
const name = data.name || 'there';

const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <style>
    body{font-family:Arial,sans-serif;background:#000;color:#fff;margin:0;padding:0}
    pre{white-space:pre-wrap;background:#3B3B3B;color:#fff;padding:20px;border-radius:6px;font-size:14px;line-height:1.8;overflow-x:auto}
  </style>
</head>
<body>
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;">
    <!-- Updated logo section -->
    <div style="text-align:center;margin-bottom:40px;">
      <img src="https://sopbuilder.oloxa.ai/logo.png" alt="OLOXA" style="height:40px;">
    </div>

    <h1 style="color:#fff;font-size:28px;text-align:center;">Congratulations, ${name}! Your SOP is Strong</h1>

    <div style="font-size:64px;font-weight:bold;color:#F26B5D;text-align:center;margin:30px 0;">${score}%</div>

    <div style="text-align:center;font-size:18px;color:#fff;margin-bottom:15px;">Your SOP Completeness Score</div>

    <div style="text-align:center;font-size:20px;color:#F26B5D;font-weight:bold;margin-bottom:40px;">You are Ready for Automation!</div>

    <div style="margin:30px 0;padding:25px;background:#1a1a1a;border-left:4px solid #F26B5D;border-radius:4px;">
      <h2 style="color:#F26B5D;font-size:20px;margin-top:0;">Your Goal</h2>
      <p><strong style="color:#F26B5D;">Intention:</strong> ${data.goal||''}</p>
      <p><strong style="color:#F26B5D;">Department:</strong> ${data.department||''}</p>
      <p><strong style="color:#F26B5D;">Who will use this:</strong> ${data.end_user||'Not specified'}</p>
      <p><strong style="color:#F26B5D;">Your Focus:</strong> ${data.improvement_type||''}</p>
    </div>

    <!-- NEW: Show improved SOP before CTA -->
    <div style="margin:30px 0;padding:25px;background:#1a1a1a;border-left:4px solid #F26B5D;border-radius:4px;">
      <h2 style="color:#F26B5D;font-size:20px;margin-top:0;">Here's Your Improved SOP</h2>
      <div style="background:#2a2a2a;border-left:4px solid #d4af37;padding:15px;margin:15px 0;border-radius:4px;font-size:14px;">
        <strong>Note:</strong> This is a guide to help you restructure your SOP. Fill in details from your own business.
      </div>
      <pre>${data.improved_sop||''}</pre>
    </div>

    <!-- Updated CTA section -->
    <div style="background:linear-gradient(135deg,#F26B5D,#ff8577);padding:30px;text-align:center;margin:40px 0;border-radius:10px;">
      <p style="color:#000;font-size:18px;font-weight:bold;margin:15px 0;">You've built a solid SOP. If you're interested in what automation could look like for this process, let's talk.</p>
      <a href="https://calendly.com/sway-oloxa/discovery-call" style="display:inline-block;background:#d4af37;color:#000;text-decoration:none;font-weight:bold;font-size:18px;padding:15px 35px;border-radius:10px;">Book Your Free Discovery Call</a>
    </div>

    <div style="text-align:center;color:#3B3B3B;font-size:12px;margin-top:40px;border-top:1px solid #3B3B3B;padding-top:20px;">© 2026 OLOXA.AI</div>
  </div>
</body>
</html>`;

return [{ json: { ...data, html_report: html, email_subject: 'Congratulations! Your SOP Scored ' + score + '%' } }];
