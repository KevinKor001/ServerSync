pkgname=ServerSync
pkgver=1.0.0
pkgrel=1
pkgdesc="A tool to simply manage & Sync files and directories to remotes with configs!"
arch=('any')
url="https://github.com/youruser/your-tool"
license=('MIT')
depends=('bash, python3') # Add runtime dependencies here
makedepends=('git' 'gcc') # Add build-time dependencies here
source=("https://github.com/youruser/$pkgname/archive/v$pkgver.tar.gz")
sha256sums=('SKIP') # We will fix this in the next step

build() {
  cd "$pkgname-$pkgver"
  make # Or your specific build command
}

package() {
  cd "$pkgname-$pkgver"
  # This installs the binary to /usr/bin inside the package
  install -Dm755 your-binary-name "$pkgdir/usr/bin/your-binary-name"
}
