const base = [];
const prot = [];
const deut = [];
const trit = [];

const canvas = document.getElementById("canvas"),
  context = canvas.getContext("2d");

const draw_image = (context) => {
  base_image = new Image();
  base_image.src = "images/espectros_line.jpg";
  base_image.onload = () => {
    context.drawImage(base_image, 0, 0);
    const base_colors = context.getImageData(0, 0, 351, 1).data;
    const prot_colors = context.getImageData(0, 1, 351, 1).data;
    const deut_colors = context.getImageData(0, 2, 351, 1).data;
    const trit_colors = context.getImageData(0, 3, 351, 1).data;

    for (let i = 0, n = base_colors.length; i < n; i += 4) {
      base.push([base_colors[i], base_colors[i + 1], base_colors[i + 2]]);
      prot.push([prot_colors[i], prot_colors[i + 1], prot_colors[i + 2]]);
      deut.push([deut_colors[i], deut_colors[i + 1], deut_colors[i + 2]]);
      trit.push([trit_colors[i], trit_colors[i + 1], trit_colors[i + 2]]);
    }

    console.log(JSON.stringify({ base, prot, deut, trit }));
  };
};

draw_image(context);
