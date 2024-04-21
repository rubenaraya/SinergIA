// frontend\jsinergia\_encriptar.js

function encriptar(textoOriginal, claveCifrado) {
    let resultado = '';
    for (let i = 0; i < textoOriginal.length; i++) {
        resultado += String.fromCharCode(textoOriginal.charCodeAt(i) ^ claveCifrado.charCodeAt(i % claveCifrado.length));
    }
    return btoa(resultado);
}
function depurarUrl(url) {
    url = url.replace('http://', '').replace('https://', '');
    url = url.replace(/[\s/.]/g, '');
    return url.replace(/[^\x00-\x7F]/g, '');
}
function dividirInvertirCadena(cadena) {
    const trozos = [];
    for (let i = 0; i < cadena.length; i += 10) {
        trozos.push(cadena.substring(i, i + 10));
    }
    const trozosInvertidos = trozos.reverse();
    const resultadoFormateado = trozosInvertidos.map(trozo => `"${trozo}"`).join(",");
    return resultadoFormateado;
}

//const textoOriginal = 'app-key-pruebas';
const textoOriginal = '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';
const urlApi = 'https://localhost/JSinergIA';

const claveCifrado = depurarUrl(urlApi);
const textoEncriptado = encriptar(textoOriginal, claveCifrado);
const resultado = dividirInvertirCadena(textoEncriptado);
console.log(resultado.toString());
