const bcrypt = require('bcryptjs');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Create default super admin
  const hashedPassword = await bcrypt.hash('admin123456', 12);

  const admin = await prisma.user.upsert({
    where: { email: 'admin@ainews.com' },
    update: {},
    create: {
      email: 'admin@ainews.com',
      password: hashedPassword,
      firstName: 'Super',
      lastName: 'Admin',
      role: 'SUPER_ADMIN',
      isActive: true,
    },
  });

  console.log(`✅ Admin user created: ${admin.email}`);

  // Create default AI settings
  const settings = await prisma.aiSettings.upsert({
    where: { id: 1 },
    update: {},
    create: {
      contentService: 'openai',
      imageService: 'gemini',
      openaiModel: 'gpt-4',
      geminiModel: 'gemini-pro',
    },
  });

  console.log(`✅ Default AI settings created (id: ${settings.id})`);

  // Create default news prompt record
  const prompt = await prisma.newsPrompt.upsert({
    where: { id: 1 },
    update: {},
    create: {
      previewContentPrompt: 'Write a professional news article preview for the upcoming match between {home_team} and {away_team}.',
      reviewContentPrompt: 'Write a professional match review article for the game between {home_team} and {away_team}.',
      transferContentPrompt: 'Write a professional transfer news article about {player_name} moving from {from_team} to {to_team}.',
    },
  });

  console.log(`✅ Default news prompts created (id: ${prompt.id})`);
  console.log('🎉 Seeding complete!');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
