const { format } = require('date-fns'); // dependência ausente do package.json

// TODO: tratar fuso horário
function hoje() {
  return format(new Date(), 'yyyy-MM-dd');
}

console.log(hoje());
