## 2.0.0 (2022-08-14)

### Features

- Upgrade endpoints to v6
- New functions:
  - `getApp(app: string)`
  - `unusedSponsorships(app: string)`,
  - `userVerificationStatus(app: string, appUserId: string, params?: { includeHash?: boolean; signed?: "eth" | "nacl"; timestamp?: "seconds" | "milliseconds"; })`
  - `userSponsorshipStatus(appUserId: string)`
