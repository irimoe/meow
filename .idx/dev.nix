{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    (pkgs.python312.withPackages (ps: with ps; [
        pandas
        ipykernel
    ]))
  ];

  idx = {
    extensions = [
      "ms-python.debugpy"
      "ms-python.python"
      "ms-toolsai.jupyter"
      "ms-toolsai.jupyter-keymap"
      "ms-toolsai.jupyter-renderers"
      "ms-toolsai.vscode-jupyter-cell-tags"
      "ms-toolsai.vscode-jupyter-slideshow"
    ];
  };
}