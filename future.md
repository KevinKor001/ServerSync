# ServerSync - Future Features & Improvements

## Security Enhancements
- [ ] **Encrypted Credentials Storage** - Replace plaintext password storage with encrypted config (use bcrypt or similar)
  - Store credentials in system keyring instead of config file
  - Implement secure credential prompting with masked input
- [ ] **SSH Key Authentication** - Support SSH key-based auth as alternative to password
- [ ] **Config File Encryption** - Encrypt `.SyncNode.config` files
- [ ] **Permission Validation** - Check local file permissions before attempting sync

## Core Functionality
- [ ] **Selective Sync Patterns** - Add `.SyncNodeIgnore` file (like `.gitignore`) to exclude patterns
- [ ] **Bidirectional Sync** - Support pulling files from server to local
- [ ] **Differential/Delta Sync** - Only sync changed files (hash-based comparison)
- [ ] **Dry-run Mode** - Preview what would be synced without actually uploading
- [ ] **Resume Interrupted Transfers** - Handle partial uploads and resume capability
- [ ] **File Filtering** - Sync only specific file types or sizes

## Monitoring & Sync Automation
- [ ] **Watch Mode** - Monitor local directory and auto-sync on file changes (using watchdog)
- [ ] **Scheduled Sync** - Cron-like scheduling for automatic syncs
- [ ] **Sync History/Log** - Detailed sync logs with timestamps and status
- [ ] **Real-time Notifications** - Terminal/desktop notifications on sync events
- [ ] **Conflict Resolution** - Handle file conflicts (overwrite, skip, merge strategies)

## User Experience
- [ ] **Config Management Commands** - Add commands to edit/view/delete configs without re-running init
  - `ServerSync config list` - List all sync nodes
  - `ServerSync config edit <name>` - Edit specific node config
  - `ServerSync config remove <name>` - Remove a config
- [ ] **Multi-Node Support** - Manage multiple server profiles
- [ ] **Status Command** - `ServerSync status` to check server connection and config
- [ ] **Verbose Output** - Better terminal formatting and colored output (improve rich usage)
- [ ] **Help System** - Comprehensive help text for each command
- [ ] **Interactive Menu** - Main menu to browse options instead of just CLI args

## Advanced Features
- [ ] **Compression** - Compress files before transfer (especially for large batches)
- [ ] **Bandwidth Limiting** - Throttle upload speeds to prevent overload
- [ ] **Parallel Transfers** - Upload multiple files concurrently
- [ ] **Sync Profiles** - Create preset sync configurations
- [ ] **Undo/Rollback** - Keep manifest of what was synced and ability to rollback
- [ ] **File Permissions Sync** - Mirror file permissions from local to remote
- [ ] **Remote Cleanup** - Option to delete remote files that don't exist locally

## Code Quality
- [ ] **Error Handling** - Comprehensive error messages and recovery
- [ ] **Unit Tests** - Test coverage for core sync logic
- [ ] **Logging Improvements** - Better logging verbosity levels
- [ ] **Documentation** - Proper docstrings and API documentation
- [ ] **Config Validation** - Validate config before using it
- [ ] **Type Hints** - Add Python type annotations throughout

## Stability & Reliability
- [ ] **Connection Pooling** - Reuse SSH connections efficiently
- [ ] **Timeout Handling** - Better handling of network timeouts
- [ ] **Retry Logic** - Automatic retry with exponential backoff for failed transfers
- [ ] **Atomic Operations** - Ensure sync operations are atomic (all or nothing)
- [ ] **Lock Files** - Prevent concurrent syncs on same node

## Distribution & Setup
- [ ] **Pip/PyPI Package** - Make installable via pip
- [ ] **System Daemon** - Option to run as background service
- [ ] **Setup Wizard Completion** - Finish the incomplete `setup.py` implementation
- [ ] **Platform Support** - Test on Windows, macOS, Linux fully
- [ ] **Requirements File** - Create proper `requirements.txt` or `pyproject.toml`

## Additional Protocols
- [ ] **SCP Support** - Alternative to SFTP
- [ ] **AWS S3 Support** - Sync to cloud storage
- [ ] **SMB/CIFS Support** - For Windows network shares
- [ ] **WebDAV Support** - Support for WebDAV servers

## Monitoring Dashboard (Future)
- [ ] **Web UI** - Simple web interface to manage syncs
- [ ] **Metrics** - Track upload speeds, success rates, timing
- [ ] **Activity Feed** - See recent sync activities and status
