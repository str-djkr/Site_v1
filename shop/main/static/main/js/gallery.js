// JavaScript-код
let selectedColor = null;
let selectedMaterial = null;

function selectColor(color) {
  if (selectedColor === color) {
    // Вже вибрано, знімаємо виділення
    selectedColor = null;
    document.getElementById(`color-${color}`).classList.remove('selected');
  } else {
    // Вибираємо новий колір
    selectedColor = color;
    document.getElementById(`color-${color}`).classList.add('selected');
  }
}

function selectMaterial(material) {
  if (selectedMaterial === material) {
    // Вже вибрано, знімаємо виділення
    selectedMaterial = null;
    document.getElementById(`material-${material}`).classList.remove('selected');
  } else {
    // Вибираємо новий матеріал
    selectedMaterial = material;
    document.getElementById(`material-${material}`).classList.add('selected');
  }
}