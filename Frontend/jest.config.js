module.exports = {
  preset: 'jest-preset-angular',
  roots: ['<rootDir>/src/'],
  testMatch: ['**/+(*.)+(spec).+(ts)'],
  setupFilesAfterEnv: ['<rootDir>/setup-jest.ts'],
  collectCoverage: true,
  coverageDirectory: './coverage',
  coverageReporters: ['clover', 'json', 'lcov', 'text', 'text-summary'],
  testResultsProcessor: 'jest-sonar-reporter',
  testTimeout: 180 * 1000,
  maxWorkers: 6,
  workerIdleMemoryLimit: '512MB',
  moduleNameMapper: {
    '^src/(.*)$': '<rootDir>/src/$1',
    '^app/(.*)$': '<rootDir>/src/app/$1',
    '^assets/(.*)$': '<rootDir>/src/assets/$1',
    '^environments/(.*)$': '<rootDir>/src/environments/$1',
  },
};
