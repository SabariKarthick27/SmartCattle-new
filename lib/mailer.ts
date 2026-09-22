import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST ?? "smtp.gmail.com",
  port: Number(process.env.SMTP_PORT ?? 587),
  secure: false, // STARTTLS
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function sendPasswordResetEmail(to: string, resetUrl: string) {
  await transporter.sendMail({
    from: process.env.SMTP_FROM ?? `SmartCattle <${process.env.SMTP_USER}>`,
    to,
    subject: "Reset your SmartCattle password",
    html: `
      <div style="font-family: Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 32px 24px; background: #f8fafc; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 24px;">
          <div style="display: inline-block; background: #0F5132; color: white; font-weight: 800; font-size: 18px; padding: 10px 20px; border-radius: 12px; letter-spacing: 1px;">SC</div>
          <h2 style="color: #0f172a; margin: 12px 0 4px;">SmartCattle</h2>
          <p style="color: #64748b; font-size: 14px; margin: 0;">Password Reset Request</p>
        </div>

        <div style="background: white; border-radius: 12px; padding: 28px; border: 1px solid #e2e8f0;">
          <p style="color: #334155; font-size: 15px; margin: 0 0 16px;">Hi,</p>
          <p style="color: #334155; font-size: 15px; margin: 0 0 24px;">
            We received a request to reset your SmartCattle password.
            Click the button below to set a new password. This link expires in <strong>1 hour</strong>.
          </p>

          <div style="text-align: center; margin: 28px 0;">
            <a href="${resetUrl}" style="display: inline-block; background: #0F5132; color: white; font-weight: 600; font-size: 15px; padding: 14px 32px; border-radius: 10px; text-decoration: none;">
              Reset Password →
            </a>
          </div>

          <p style="color: #94a3b8; font-size: 12px; margin: 24px 0 0; border-top: 1px solid #f1f5f9; padding-top: 16px;">
            If you didn't request this, you can safely ignore this email. Your password won't be changed.
          </p>
          <p style="color: #94a3b8; font-size: 11px; margin: 8px 0 0; word-break: break-all;">
            Or copy this link: ${resetUrl}
          </p>
        </div>
      </div>
    `,
    text: `Reset your SmartCattle password\n\nClick the link below (expires in 1 hour):\n${resetUrl}\n\nIf you didn't request this, ignore this email.`,
  });
}
