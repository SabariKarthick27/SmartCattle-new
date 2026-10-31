import prisma from "../lib/prisma";

async function main() {
  await prisma.user.deleteMany({
    where: { email: "vet@smartcattle.com" },
  });
  console.log("Deleted vet@smartcattle.com successfully.");
}

main().catch(console.error);
