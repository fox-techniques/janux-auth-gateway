# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/fox-techniques/janux-auth-gateway/compare/v1.0.0...HEAD)</small>

### Added

- Add email masking utility and update logging for admin and test user account creation ([fac4991](https://github.com/fox-techniques/janux-auth-gateway/commit/fac499195a383d501c86e35724830c4147b86249) by A Nova).

### Removed

- Remove email from admin and user account creation logging ([c945dd1](https://github.com/fox-techniques/janux-auth-gateway/commit/c945dd13a80d66c1882b4ffb5273e07e499e8229) by A Nova).

<!-- insertion marker -->
## [v1.0.0](https://github.com/fox-techniques/janux-auth-gateway/releases/tag/v1.0.0) - 2025-02-02

<small>[Compare with v0.1.3](https://github.com/fox-techniques/janux-auth-gateway/compare/v0.1.3...v1.0.0)</small>

## [v0.1.3](https://github.com/fox-techniques/janux-auth-gateway/releases/tag/v0.1.3) - 2025-02-02

<small>[Compare with v0.1.2](https://github.com/fox-techniques/janux-auth-gateway/compare/v0.1.2...v0.1.3)</small>

## [v0.1.2](https://github.com/fox-techniques/janux-auth-gateway/releases/tag/v0.1.2) - 2025-02-02

<small>[Compare with v0.1.1](https://github.com/fox-techniques/janux-auth-gateway/compare/v0.1.1...v0.1.2)</small>

## [v0.1.1](https://github.com/fox-techniques/janux-auth-gateway/releases/tag/v0.1.1) - 2025-02-02

<small>[Compare with v0.1.0](https://github.com/fox-techniques/janux-auth-gateway/compare/v0.1.0...v0.1.1)</small>

### Removed

- Remove backward compatibility tests from GitHub Actions workflow and adjust dependencies in tox.ini ([12ae991](https://github.com/fox-techniques/janux-auth-gateway/commit/12ae991c2d88cf9782a91e76238fb59f1d10599a) by A Nova).

## [v0.1.0](https://github.com/fox-techniques/janux-auth-gateway/releases/tag/v0.1.0) - 2025-02-02

<small>[Compare with first commit](https://github.com/fox-techniques/janux-auth-gateway/compare/236ab30b96567572943499d47db3769df44a7c09...v0.1.0)</small>

### Added

- Add GitHub Actions workflow for publishing to PyPI with version checks and backward compatibility tests ([93ee7b3](https://github.com/fox-techniques/janux-auth-gateway/commit/93ee7b39bc319c7ebc85f45ef2e1454736225149) by A Nova).
- Add usage guide for JANUX Authentication Gateway with API endpoints and examples ([3b49ce9](https://github.com/fox-techniques/janux-auth-gateway/commit/3b49ce9dbdb841fa219e960b03df95f1f6cfc8cd) by A Nova).
- Add pytest configuration and enhance test fixtures; update user model fields for better schema examples for Pydantic v2+ and tox for backwards compatibility ([74373cd](https://github.com/fox-techniques/janux-auth-gateway/commit/74373cd62c02e8a354314728699f006e94a0730f) by A Nova).
- Add AES encryption settings and key pair generation functionality; update documentation and configuration files ([4b33032](https://github.com/fox-techniques/janux-auth-gateway/commit/4b33032e43d95848c65fae404570354bce07f111) by A Nova).
- Add Redis configuration and enhance MongoDB initialization; update password security checks and example environment file ([b0d7397](https://github.com/fox-techniques/janux-auth-gateway/commit/b0d73976edc3100758d8e355c264e122e4fd3956) by A Nova).
- Add CORS configuration and security warnings; implement unit tests for admin and user API routes. Unittesting is finished ([3a6b880](https://github.com/fox-techniques/janux-auth-gateway/commit/3a6b880227b7f80d0e23f856b8684c3496c9bb7f) by A Nova).
- Add unit tests for role enumerations and enhance validation for Admin and User models ([2653a4e](https://github.com/fox-techniques/janux-auth-gateway/commit/2653a4eb92ab078439eea122a2e581a33ddb0ae3) by A Nova).
- Add tester account creation and unique email index for Admin and User models; update documentation and configuration ([f25621c](https://github.com/fox-techniques/janux-auth-gateway/commit/f25621cd7ea3dfc615bde48a19e42f9c79a5f95b) by A Nova).
- Add unit tests for MongoDB initialization, super admin creation, and user/admin authentication ([be1ccb4](https://github.com/fox-techniques/janux-auth-gateway/commit/be1ccb44790a58fdd224359768bbc3d8574b7e29) by A Nova).
- Add unit tests for JWT authentication, password hashing, and configuration retrieval modules ([fa688be](https://github.com/fox-techniques/janux-auth-gateway/commit/fa688be1a939d4aefe64bfb9a7414e7ff564e90f) by A Nova).
- Add ALLOWED_ORIGINS configuration for CORS support; update .env.example and modify middleware to use dynamic origins. ([f5ca789](https://github.com/fox-techniques/janux-auth-gateway/commit/f5ca789614b5d7bf12445f19c6dc31bf7c897aa4) by A Nova).
- Add unit tests for JANUX Authentication Gateway API routes, token schema, role enumerations, response schemas, and main application; update VSCode settings for pytest integration. ([97aa837](https://github.com/fox-techniques/janux-auth-gateway/commit/97aa837d70f454e7056e384803a02342218abdc9) by A Nova).
- Add secrets management and unit tests for authentication and configuration modules; update .gitignore to include secrets, create example secrets file, and enhance testing for password hashing and configuration retrieval. ([0e16a19](https://github.com/fox-techniques/janux-auth-gateway/commit/0e16a19f68d1d32d8fb897962c9832b9f90ff26b) by A Nova).
- Add admin model and router with role-based access control; update configuration for super admin credentials ([c9da0a3](https://github.com/fox-techniques/janux-auth-gateway/commit/c9da0a36ddad39b30a436e06f1cf5caa3066c675) by A Nova).
- Add initial structure for authentication microservice with FastAPI, including models, schemas, routers, and logging setup ([5d9db43](https://github.com/fox-techniques/janux-auth-gateway/commit/5d9db43a86494746fbe44d38aa4e68e47ac05d6a) by A Nova).
- Add frontend setup with React, TypeScript, and Vite ([9427809](https://github.com/fox-techniques/janux-auth-gateway/commit/942780950127f07ca99741a54cca355a919e2f33) by A Nova).
- Add MongoDB integration and user registration functionality ([97e2b78](https://github.com/fox-techniques/janux-auth-gateway/commit/97e2b780382e180110b709624498cc26ad86280d) by A Nova).
- Add initial backend structure with FastAPI setup and logging configuration ([2819966](https://github.com/fox-techniques/janux-auth-gateway/commit/28199668e7dce4c7673feb303c6c2d7687e5c863) by A Nova).

### Fixed

- Fix typos and enhance community support documentation; update Discord link and add Slack community invitation ([b4233ee](https://github.com/fox-techniques/janux-auth-gateway/commit/b4233eeb27e9054d346eb2106e0d01984577d9c4) by A Nova).

### Removed

- Remove unused full name validator from User and Admin models; update pymdown-extensions to version 10.14.2; delete obsolete unit tests for base router, token schema, role enumerations, and response schemas. ([8dcf027](https://github.com/fox-techniques/janux-auth-gateway/commit/8dcf027e373ee6b50e4d45c69899bd8123f52c8e) by A Nova).
- Remove unused files and configurations; delete obsolete modules, update project structure, and add example environment file ([8a66766](https://github.com/fox-techniques/janux-auth-gateway/commit/8a66766f7e9b708f12b536d9b48c55b18bd1d600) by A Nova).

