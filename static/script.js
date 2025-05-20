import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_KEY = process.env.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;
const REFERER = "https://your-site-url.com";
const TITLE = "BReady";

app.use(express.json());

app.post('/api/steps', async (req, res) => {
  const { goal } = req.body;

  if (!goal) {
    return res.status(400).json({ error: 'Goal is required.' });
  }

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': REFERER,
        'X-Title': TITLE
      },
      body: JSON.stringify({
        model: 'openai/gpt-4o',
        messages: [
          {
            role: 'user',
            content: `Give me a step-by-step plan to achieve the goal: ${goal}`
          }
        ]
      })
    });

    const data = await response.json();
    const content = data?.choices?.[0]?.message?.content || 'No steps returned.';
    const steps = content.split('\n').filter(line => line.trim());

    res.json({ steps });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to fetch steps.' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});