// frontend\jsinergia\DefinicionModulo.js

export class DefinicionModulo {
    constructor() {
        this.definiciones = new Map();
        this._registrarDefiniciones();
    }
    // Funciones privadas compartidas por todas las subclases
    _registrarDefiniciones() {
        this.definiciones.set('ManejadoresInteracciones', this.manejadoresInteracciones());
        this.definiciones.set('AccionesCoordinador', this.accionesCoordinador());
        this.definiciones.set('ReaccionesCoordinador', this.reaccionesCoordinador());
        this.definiciones.set('InterfazUsuario', this.extenderInterfazUsuario());
        this.definiciones.set('OperadorDatos', this.extenderOperadorDatos());
        this.definiciones.set('PresentadorContenido', this.extenderPresentadorContenido());
        this.definiciones.set('ValidadoresDatos', this.validadoresDatos());
    }
    // Funciones públicas compartidas por todas las subclases
    traspasarDefiniciones(clave) {
        Base.trazarFlujo(this.constructor.name, 'traspasarDefiniciones', 3, clave);
        return this.definiciones.get(clave);
    }
    // Funciones públicas que deben implementar y sobreescribir obligatoriamente todas las subclases
    manejadoresInteracciones() {return {};}
    accionesCoordinador() {return {};}
    reaccionesCoordinador() {return {};}
    validadoresDatos() {return {};}
    extenderPresentadorContenido() {return {};}
    extenderInterfazUsuario() {return {};}
    extenderOperadorDatos() {return {};}
}
