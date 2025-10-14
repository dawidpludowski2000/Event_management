/** @type {import('next').NextConfig} */
module.exports = {
  // NIE przerywaj buildu przez ESLint
  eslint: {
    ignoreDuringBuilds: true,
  },
  // (opcjonalnie) jeśli będziesz miał ostrzejsze błędy TS – też nie przerywaj buildu:
  // typescript: {
  //   ignoreBuildErrors: true,
  // },
};
