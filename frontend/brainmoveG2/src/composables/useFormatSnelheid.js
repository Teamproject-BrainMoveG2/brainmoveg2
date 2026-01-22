export function formatSnelheid(label, value) {
  if (label && label.toLowerCase().includes('snelheid')) {
    console.log('formatSnelheid composable value:', value);
    if (Number(value) > 1000) {
      return (Number(value) / 1000).toFixed(2) + ' s';
    }
    return value + ' ms';
  }
  return value;
}
