{
  description = "Development environment with pixi";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = nixpkgs.lib;

        # Native libraries used by the PyQt/vispy stack from pixi. NixOS has no
        # ld.so.cache, so ctypes.util.find_library (vispy) and dlopen (Qt/GL)
        # only work when these are exported explicitly.
        qtRuntimeLibs = lib.optionals pkgs.stdenv.isLinux (with pkgs; [
          dbus
          fontconfig
          freetype
          glib
          libGL
          libxkbcommon
          mesa
          stdenv.cc.cc.lib
          wayland
          xorg.libX11
          xorg.libXcomposite
          xorg.libXext
          xorg.libxcb
          xorg.xcbutilcursor
          xorg.xcbutilimage
          xorg.xcbutilkeysyms
          xorg.xcbutilrenderutil
          xorg.xcbutilwm
          zlib
          zstd
        ]);
        qtLibraryPath = lib.makeLibraryPath qtRuntimeLibs;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pre-commit
            pixi
          ];

          # export SHELL=${lib.getExe pkgs.bash}
          shellHook = ''
            export PS1="(nix-dev) \u@\h:\w\$ "
            ${lib.optionalString pkgs.stdenv.isLinux ''
              export LD_LIBRARY_PATH="${qtLibraryPath}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
              export LIBRARY_PATH="${qtLibraryPath}''${LIBRARY_PATH:+:$LIBRARY_PATH}"
              export LIBGL_DRIVERS_PATH="${pkgs.mesa}/lib/dri''${LIBGL_DRIVERS_PATH:+:$LIBGL_DRIVERS_PATH}"
              export __EGL_VENDOR_LIBRARY_FILENAMES="${pkgs.mesa}/share/glvnd/egl_vendor.d/50_mesa.json''${__EGL_VENDOR_LIBRARY_FILENAMES:+:$__EGL_VENDOR_LIBRARY_FILENAMES}"
              # Keep host Qt plugins (e.g. KDE's Qt 6 plugins) away from the
              # PyQt5 bundled in the pixi environment.
              unset QT_PLUGIN_PATH QML2_IMPORT_PATH
            ''}
            echo "Development environment with pixi is ready!"
            echo "Run 'pixi shell --environment development' to start the pixi shell for development."
          '';
        };
      });
}
