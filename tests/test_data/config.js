// Test configuration with fake secrets
const config = {
  // AWS credentials (fake)
  aws: {
    accessKeyId: 'AKIAI_placeholder',
    secretAccessKey: 'wJalrXU_placeholder'
  },

  // Stripe keys (fake)
  stripe: {
    publicKey: 'pk_test_5_placeholder',
    secretKey: 'sk_test_5_placeholder'
  },

  // Database URL (fake)
  database: {
    url: 'postgres://username:password@localhost:5432/mydb'
  },

  // JWT secret (fake)
  jwt: {
    secret: 'mySuperSecretJWTKeyThatIsVeryLongAndSecure123!'
  },

  // Generic API key (fake)
  apiKey: 'abc123def456gh_placeholder'
};
