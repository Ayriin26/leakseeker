// Test configuration with fake secrets
const config = {
  // AWS credentials (fake)
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
  },

  // Stripe keys (fake)
  stripe: {
    publicKey: 'pk_test_51ABC123xyz789fakekey123',
    secretKey: 'sk_test_51ABC123xyz789fakekey456'
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
  apiKey: 'abc123def456ghi789jkl012mno345pqr678stu901'
};
