const base = [];
const prot = [];
const deut = [];
const trit = [];

const canvas = document.getElementById("canvas"),
  context = canvas.getContext("2d");

const transformColor = (color, transformBy) => {
  const newColor = Math.floor(color * transformBy);
  if (newColor > 255) return 255;
  if (newColor < 0) return 0;
  return newColor;
};

const getLighterColors = (colors) => {
  const lighterColors = colors.map(([r, g, b]) => [
    transformColor(r, 1.4),
    transformColor(g, 1.4),
    transformColor(b, 1.4),
  ]);
  return lighterColors;
};

const getDarkerColors = (colors) => {
  const darkerColors = colors.map(([r, g, b]) => [
    transformColor(r, 0.6),
    transformColor(g, 0.6),
    transformColor(b, 0.6),
  ]);
  return darkerColors;
};

const generateCommomColors = () => {
  return Array.from(Array(25))
    .map(() => {
      const number = Math.round(Math.random() * 255);
      return [number, number, number];
    })
    .concat([
      [0, 0, 0],
      [255, 255, 255],
    ]);
};

const commomColors = generateCommomColors();

console.log({ commomColors });

const draw_image = (context) => {
  base_image = new Image();
  base_image.src = "images/espectros-line.png";
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

    base.push(
      ...getLighterColors(base),
      ...getDarkerColors(base),
      ...commomColors
    );
    prot.push(
      ...getLighterColors(prot),
      ...getDarkerColors(prot),
      ...commomColors
    );
    deut.push(
      ...getLighterColors(deut),
      ...getDarkerColors(deut),
      ...commomColors
    );
    trit.push(
      ...getLighterColors(trit),
      ...getDarkerColors(trit),
      ...commomColors
    );

    console.log(JSON.stringify({ base, prot, deut, trit }));
  };
};

draw_image(context);
