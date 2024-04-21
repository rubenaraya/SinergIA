// frontend\jsinergia\BibliotecaBase.js

/* **************************************************************************** */
/* JSinergIA: BIBLIOTECA JAVASCRIPT PARA APLICACIONES WEB DE FRONT-END

PRESENTACION
JSinergIA es una biblioteca JavaScript avanzada y multifacética, diseñada con el propósito de ofrecer una solución integral para el desarrollo, ensamblaje y adaptación de Aplicaciones Web de una Sola Página (SPA) y Aplicaciones Web Progresivas (PWA).
Aunque se inspiró inicialmente en el patrón "Modelo-Vista-Presentador" (MVP), JSinergIA ha evolucionado para integrar elementos de arquitectura limpia, arquitectura hexagonal, Domain-Driven Design (DDD), arquitectura orientada a eventos y patrones reactivos, enriqueciéndose con un sofisticado sistema de publicación/suscripción asincrónico y multi-direccional. Este concepto de "Arquitectura Híbrida, Reactiva y Multidimensional", aumenta la gama de interacciones posibles y promueve un enfoque más flexible y distribuido sobre los flujos de datos y eventos, acomodándose a diferentes escenarios de uso y requerimientos de desarrollo.
JSinergIA ofrece un conjunto de herramientas optimizadas para crear aplicaciones web modulares, robustas, personalizables y reutilizables. Su diseño adaptable y extensible implementa características muy potentes, como la configuración basada en datos, la importación dinámica de componentes, el modelado independiente de la lógica del dominio, el polimorfismo de la UI según los roles del usuario, junto con la posibilidad de integrar diversas API de back-end mediante adaptadores. Todo lo anterior multiplica las oportunidades para realizar una personalización profunda y ágil y poder aplicar patrones arquitectónicos más complejos.
Pero más allá de estas características funcionales, JSinergIA ha sido ideada como una biblioteca amistosa y usable para desarrolladores/as, enfocada en mejorar sus experiencias de usuario durante la construcción de aplicaciones web modernas, ayudándoles a reducir la complejidad inherente a este proceso para poder centrarse en modelar la lógica del dominio de negocio y diseñar la experiencia de los usuarios finales. Finalmente, lo que pretende es contribuir a que las aplicaciones desarrolladas sean más simples, ordenadas, comprensibles y fáciles de mantener, a lo largo de todo su ciclo de vida (y con la menor cantidad de código que sea posible).

ORIGEN DEL NOMBRE JSinergIA
El nombre JSinergIA nace de una fusión creativa y significativa entre dos elementos esenciales en su desarrollo: JavaScript ("JS") e Inteligencia Artificial ("IA"). Esta combinación no es solo un juego de palabras, sino que encapsula la esencia colaborativa entre el ingenio humano y las capacidades avanzadas de la inteligencia artificial. La palabra "sinergia" refleja la filosofía central de la biblioteca: diferentes componentes trabajando en armonía para lograr un resultado que trasciende la suma de sus partes individuales. En el desarrollo de JSinergIA, la interacción entre el desarrollador humano y las herramientas de inteligencia artificial ha sido clave para optimizar, refinar y expandir sus funcionalidades, convirtiéndola en un testimonio del potencial ilimitado de esta colaboración. JSinergIA simboliza, por tanto, un modelo a seguir en el desarrollo de software, donde la sinergia entre inteligencia humana e inteligencia artificial abre nuevas fronteras en el diseño y la implementación de aplicaciones.

CARACTERISTICAS TECNICAS
JSinergIA adhiere a varios estándares técnicos, patrones de diseño y buenas prácticas de programación, lo que contribuye a su calidad, mantenibilidad y escalabilidad como biblioteca de software. Algunos de estos aspectos son:
1. Patrón Modelo-Vista-Presentador (MVP): La biblioteca se estructura siguiendo en su núcleo el patrón MVP, lo que facilita la separación de responsabilidades entre la lógica de negocio, la interfaz de usuario y la presentación de los flujos operacionales, lo que mejora la capacidad de prueba y mantenimiento del código.
2. Arquitectura Modular y Cohesiva: La biblioteca se caracteriza por una arquitectura modular que facilita la extensión y mantenimiento. Cada componente tiene responsabilidades bien definidas, lo que permite reutilizar y personalizar partes de la aplicación de forma independiente.
3. Programación Orientada a Objetos (POO): La biblioteca hace uso extensivo de la POO, lo que permite una organización clara del código, facilita la reutilización y promueve el encapsulamiento y la abstracción.
4. Principios SOLID: Los principios SOLID de diseño de software orientado a objetos se aplican en la biblioteca para promover un diseño más limpio y manejable. Esto incluye los principios de: responsabilidad única (SRP), abierto a extensión / cerrado a modificación (OCP), sustitución de Liskov (LSP), segregación de interfaces (ISP) y la inversión de dependencias (DIP).
5. Patrón de Publicación/Suscripción: Para la gestión de eventos y la comunicación entre componentes, se utiliza un sistema de publicación/suscripción multi-direccional, lo que permite una comunicación desacoplada y mejora la capacidad de respuesta de las aplicaciones.
6. Control de Acceso Basado en Roles (RBAC): Implementa RBAC de manera robusta, flexible y granular, permitiendo una gestión de seguridad efectiva y adaptada a las necesidades de aplicaciones complejas, para garantizar la seguridad y el acceso apropiado a sus funcionalidades según los perfiles y roles de los diferentes usuarios.
7. Adaptadores para la Integración de APIs: La utilización de adaptadores para la conexión con diversas APIs de back-end sigue el patrón de diseño de adaptador, proporcionando una interfaz unificada para la interacción con diferentes fuentes de datos y servicios externos, y mejorando con ello la interoperabilidad.
8. Estándares de Codificación: La biblioteca sigue estándares de codificación claros y consistentes, como la nomenclatura adecuada, el empleo de estilos de codificación modernos y concisos, la organización lógica del código y la documentación interna, lo que ayuda a la legibilidad y el mantenimiento. Todos los nombres de clases, funciones y variables definidos en el código están en español, para facilitar su comprensión y aprendizaje para un público no especializado.
9. Gestión de Estado y Contexto: Manejo avanzado del estado global y contexto particular de la aplicación, crucial en SPAs y PWAs, siguiendo principios de inmutabilidad y transparencia en la transferencia de estados.
10. Sistema integrado de Gestión de Errores: Implementa un sistema estructurado y coherente para la gestión de errores, lo que aumenta la robustez y fiabilidad de las aplicaciones.
11. Modularidad y Extensibilidad: La estructura modular de la biblioteca y su diseño orientado a la extensibilidad hacen que sea adaptable a diferentes contextos y necesidades, facilitando la incorporación de nuevas funcionalidades y servicios según los requerimientos de cada proyecto.
12. Soporte para Internacionalización y Localización: La biblioteca está diseñada para manejar múltiples idiomas y configuraciones locales en forma desacoplada del código fuente.
13. Diseño basado en Dominios (DDD): La biblioteca adopta principios de Domain-Driven Design (DDD) para modelar la lógica del dominio, a través de la creación y gestión de sus "esquemas de dominio" que representan la esencia de la lógica del dominio de cada servicio, proporcionando una separación clara y un desacoplamiento efectivo de la capa del dominio respecto a otras capas de la arquitectura.

LICENCIA DE USO
Este software fue desarrollado por Rubén Araya Tagle (c) 2024, con la asistencia y colaboración de ChatGPT (GPT-4), un Modelo de Lenguaje de OpenAI. Este proyecto es un testimonio de la sinergia entre la creatividad humana y la inteligencia artificial, y se ofrece bajo la Licencia MIT para fomentar su uso, estudio, modificación y distribución de manera abierta y accesible.
*/

/* **************************************************************************** */
/* CLASES PRINCIPALES: CoordinadorGeneral, OperadorDatos, InterfazUsuario */

/* CLASE: CoordinadorGeneral [singleton] (extensible)
PROPOSITO: Coordinar las interacciones entre los diferentes componentes de la aplicación, actuando como su núcleo central y punto de inicio, manejando el flujo de datos y eventos entre la interfaz de usuario, el manejo de estado y los servicios de datos.
RESPONSABILIDADES:
1. Gestión de Estado: Mantiene y actualiza el estado global de la aplicación, garantizando la coherencia a lo largo de todo el flujo de trabajo.
2. Coordinación de Interacciones: Maneja las interacciones del usuario, delegando acciones a otros componentes como InterfazUsuario y OperadorDatos.
3. Control de Flujo de Datos: Orquesta el flujo de datos entre la interfaz de usuario y los servicios de back-end, asegurando que los datos correctos se entreguen en el momento adecuado.
4. Integración de Componentes: Actúa como un mediador entre diferentes componentes de la aplicación, facilitando su integración y comunicación eficiente.
5. Manejo de Eventos: Responde a eventos generados por cambios en el estado de la aplicación o por acciones del usuario, y ejecuta las acciones y reacciones correspondientes.
NOTAS: Esta clase es ampliable mediante la inyección de extensiones, a través de la configuración dinámica que se aplica al ejecutar cada servicio. Las funciones que se pueden agregar para ampliar la funcionalidad de esta clase se dividen en dos tipos principales:
- Funciones de "acciones" (activas): manejan eventos de interacción en la UI y ejecutan "acciones".
- Funciones de "reacciones" (reactivas): manejan eventos de cambios de estado (del Modelo o la Vista) y "reaccionan".
Todas estas funciones se deben agregar a subclase de "DefinicionServicio" donde se implementará cada servicio específico (dentro de "accionesCoordinador" y "reaccionesCoordinador").
*/
class CoordinadorGeneral { //(PRESENTADOR)
    constructor(operadorDatos, interfazUsuario) {
        this.interfazUsuario = interfazUsuario;
        this.operadorDatos = operadorDatos;
        this.gestorEstado = null;
        this.configuradorModulos = null;
        this.controladorAcceso = null;
        this.procesadorEsquemas = null;
        this.manejadorErrores = null;
        this.servicio = '';
        this.rutaErrores = '';
        this.INTERACCIONES = {};
        this.HISTORIAL = {};
    }
    static obtenerInstancia(operadorDatos, interfazUsuario) {
        if (!this.instancia) {
            this.instancia = new CoordinadorGeneral(operadorDatos, interfazUsuario);
        }
        return this.instancia;
    }
    // Funciones de configuración dinámica
    inyectarExtensiones(extensiones) {
        for (let nombreFuncion in extensiones) {
            if (extensiones.hasOwnProperty(nombreFuncion)) {
                let funcion = extensiones[nombreFuncion];
                if (typeof funcion === 'function') {
                    this[nombreFuncion] = funcion.bind(this);
                }
            }
        }
    }
    async coordinarInicio(rutaManifiesto, rutaErrores, gestorEstado, configuradorModulos=null, controladorAcceso=null, procesadorEsquemas=null) {
        Base.trazarFlujo(this.constructor.name, 'coordinarInicio', 1);
        try {
            if (gestorEstado && typeof gestorEstado === 'object') {
                this.gestorEstado = gestorEstado;
                this.rutaErrores = rutaErrores;
                this.manejadorErrores = new ManejadorErrores(this.interfazUsuario.traductorIdiomas, this.rutaErrores);
                this.configuradorModulos = configuradorModulos || new ConfiguradorModulos();
                this.procesadorEsquemas = procesadorEsquemas || new ProcesadorEsquemas();
                this.controladorAcceso = controladorAcceso || new ControladorAcceso(this.gestorEstado);
                this.interfazUsuario.coordinarInicio(this.gestorEstado, this.manejadorErrores);
                this.operadorDatos.coordinarInicio(this.gestorEstado, this.manejadorErrores);
                this.configuradorModulos.coordinarInicio(this.gestorEstado, this.interfazUsuario.traductorIdiomas);
                let uuid = this.gestorEstado.obtenerValor(Base.Estados.sesion, 'uuid');
                if (!uuid) {
                    uuid = Base.generarUUID();
                    this.gestorEstado.asignarValor(Base.Estados.sesion, 'uuid', uuid);
                }
                await this.operadorDatos.comunicadorApi.consultarManifiestoApp(rutaManifiesto);
                return true;
            }
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
        return false;
    }
    async ejecutarModulo(rutaModulo) {
        Base.trazarFlujo(this.constructor.name, 'ejecutarModulo', 1);
        try {
            await this.configuradorModulos.importarModulo(rutaModulo);
            const resultado = this.configuradorModulos.aplicarConfiguracion(this);
            if (resultado) {
                const rutaDominio = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'rutaDominio');
                const rolesUsuario = this.gestorEstado.obtenerValor(Base.Estados.sesion, 'roles');
                this.procesadorEsquemas.asignarParametros(rolesUsuario, rutaDominio);
            }
            return resultado;
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    async procesarEsquemas(portadorInformacion) {
        Base.trazarFlujo(this.constructor.name, 'procesarEsquemas', 1);
        try {
            this.procesadorEsquemas.asignarParametros(
                this.gestorEstado.obtenerValor(Base.Estados.sesion, 'roles'), 
                this.gestorEstado.obtenerValor(Base.Estados.modelo, 'rutaDominio')
            );
            await this.procesadorEsquemas.importarEsquemas(portadorInformacion);
            const funcionFiltro = this.controladorAcceso.filtrarPorRoles;
            this.procesadorEsquemas.filtrarEsquemas(portadorInformacion, funcionFiltro);
            return portadorInformacion.recuperarInformacion('esquemas');
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    // Funciones de control
    async lanzarInteraccion(interaccion, servicio=null) {
        Base.trazarFlujo(this.constructor.name, 'lanzarInteraccion', 1, interaccion);
        try {
            const detalleInteraccion = this.controlarAcceso(interaccion, servicio);
            if (!detalleInteraccion) { return this.rechazarAcceso(interaccion, detalleInteraccion); }
            await this[interaccion]({...detalleInteraccion});
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    controlarAcceso(interaccion, servicio=null) {
        Base.trazarFlujo(this.constructor.name, 'controlarAcceso', 1, interaccion, servicio);
        try {
            if (!servicio) {
                servicio = this.servicio;
            }
            if (!servicio || !interaccion) {
                throw new ErrorPersonalizado('ERROR_INTERACCION_NO_VALIDA', '', {}, Base.Errores.NO_VALIDO);
            }
            const mapaServicio = this.INTERACCIONES[servicio];
            if (!mapaServicio) {
                throw new ErrorPersonalizado('ERROR_INTERACCION_NO_ENCONTRADA', '', {}, Base.Errores.NO_ENCONTRADO);
            }
            const detalleInteraccion = mapaServicio.get(interaccion);
            if (!(detalleInteraccion && detalleInteraccion.permisos && typeof this[interaccion] === 'function')) {
                throw new ErrorPersonalizado('ERROR_INTERACCION_NO_PROCESABLE', '', {}, Base.Errores.NO_PROCESABLE);
            }
            const permisosAcceso = detalleInteraccion.permisos;
            const rolesCredenciales = this.gestorEstado.obtenerValor(Base.Estados.sesion, 'roles');
            const verificacion = this.controladorAcceso.autorizarPorRoles(permisosAcceso, rolesCredenciales);
            if (verificacion === true) {
                return detalleInteraccion;
            } 
            return verificacion;
        } catch (error) {
            throw error;
        }
    }
    rechazarAcceso(interaccion, detalle) {
        Base.trazarFlujo(this.constructor.name, 'rechazarAcceso', 1, interaccion);
        try {
            if (detalle === null) {
                this.interfazUsuario.mostrarInformacion(
                    this.interfazUsuario.traductorIdiomas._('ERROR_INTERACCION_NO_AUTENTICADA'),
                    Base.Mensajes.ALERTA
                );
                this.ingresarDatosIdentificacion(interaccion);
            } else if (!detalle) {
                this.interfazUsuario.mostrarInformacion(
                    this.interfazUsuario.traductorIdiomas._('ERROR_INTERACCION_NO_AUTORIZADA'),
                    Base.Mensajes.ALERTA
                );
            }
            return detalle;
        } catch (error) {
            throw error;
        }
    }
    ingresarDatosIdentificacion(interaccion='') {
        Base.trazarFlujo(this.constructor.name, 'ingresarDatosIdentificacion', 1, interaccion);
        try {
            const idFormLogin = 'form_login';
            const idBotonLogin = 'boton_login';
            let contenido = this.interfazUsuario.presentadorContenido.representarContenido('plantillaFormLogin', {"idFormLogin": idFormLogin, "idBotonLogin": idBotonLogin});
            const elemento = this.interfazUsuario.ELEMENTOS.get('area_cuerpo');
            if (elemento && contenido) {
                contenido = this.interfazUsuario.traductorIdiomas.aplicarTraduccion(contenido);
                this.interfazUsuario.manipuladorUI.actualizarContenido(elemento, contenido);
                this.interfazUsuario.manipuladorUI.cambiarVisibilidad(elemento, true, true);
                if (interaccion) {
                    this.interfazUsuario.manipuladorUI.asignarValorCampo(idFormLogin, 'interaccion', interaccion);
                }
                const botonLogin = this.interfazUsuario.manipuladorUI.seleccionar(`#${idBotonLogin}`);
                this.interfazUsuario.manipuladorUI.configurarElemento(botonLogin, {"activado": true}, this.enviarDatosIdentificacion.bind(this));
                this.interfazUsuario.manipuladorUI.enfocarEnCampo(idFormLogin, 'username');
            }
        } catch (error) {
            throw error;
        }
    }
    async enviarDatosIdentificacion() {
        Base.trazarFlujo(this.constructor.name, 'enviarDatosIdentificacion', 1);
        const areaContenido = 'area_cuerpo';
        try {
            const valores = this.interfazUsuario.receptorUI.obtenerDatosFormulario('form_login');
            const elemento = this.interfazUsuario.manipuladorUI.seleccionar('#boton_login');
            this.interfazUsuario.quitarErroresValidacion('form_login');
            if (elemento && valores) {
                const contexto = this.interfazUsuario.receptorUI.capturarDatosContexto(elemento);
                const portadorInformacion = new PortadorInformacion(this.gestorEstado);
                portadorInformacion.prepararPeticion(contexto.operacion, {
                    valores: valores,
                    recurso: contexto.recurso,
                    servicio: contexto.servicio,
                    formulario: contexto.esquema
                });
                await this.procesarEsquemas(portadorInformacion);
                if (!this.operadorDatos.comprobarDatosEnviados(portadorInformacion)) { return false; }
                this.interfazUsuario.alternarEsperando(true, areaContenido);
                const urlReceptor = Base.construirUrlAbsoluta(contexto.recurso);
                const resultado = await this.operadorDatos.comunicadorApi.enviarPeticionJson(urlReceptor, valores, 'POST');
                if (this.controladorAcceso.registrarDatosSesion(resultado)) {
                    if (resultado.mensaje) {
                        this.interfazUsuario.mostrarInformacion(resultado.mensaje, resultado.tipo);
                    }
                    this.interfazUsuario.manipuladorUI.actualizarContenido(this.interfazUsuario.ELEMENTOS.get(areaContenido), '');
                    this.interfazUsuario.alternarEsperando(false, areaContenido);
                    const interaccion = valores.interaccion || resultado.inicio;
                    if (interaccion) {
                        await this.lanzarInteraccion(interaccion);
                    }
                }
            }
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
            this.interfazUsuario.alternarEsperando(false, areaContenido);
        }
    }
    finalizarSesion(redirigir=false) {
        Base.trazarFlujo(this.constructor.name, 'finalizarSesion', 1);
        try {
            const urlSalida = this.controladorAcceso.vaciarDatosSesion();
            this.interfazUsuario.mostrarInformacion(
                this.interfazUsuario.traductorIdiomas._('SESION_FINALIZADA'),
                Base.Mensajes.AVISO
            );
            this.interfazUsuario.manipuladorUI.actualizarContenido(this.interfazUsuario.ELEMENTOS.get('area_cuerpo'), '');
            if (redirigir && urlSalida) {
                this.interfazUsuario.abrirUrl(urlSalida);
            }
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    // Funciones de gestión de errores
    informarEnvioRechazado(contexto) {
        Base.trazarFlujo(this.constructor.name, 'informarEnvioRechazado', 1);
        try {
            if (contexto.errores) {
                this.interfazUsuario.mostrarErroresValidacion(contexto.errores);
            }
            this.interfazUsuario.mostrarInformacion(
                this.interfazUsuario.traductorIdiomas._('ERROR_FORMULARIO_NO_VALIDO'),
                Base.Mensajes.ALERTA
            );
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    informarErrorModulo(errorProcesado) {
        Base.trazarFlujo(this.constructor.name, 'informarErrorModulo', 1);
        try {
            this.interfazUsuario.mostrarInformacion(errorProcesado.mensaje, errorProcesado.tipo);
            this.gestorEstado.emitirEventoInformacion('RESPUESTA_RECIBIDA', {});
        } catch (error) {
            console.error(error);
        }
    }
    // Funciones de instalación App / PWA
    async instalarAplicacion(rutaTrabajadorServicio) {
        Base.trazarFlujo(this.constructor.name, 'instalarAplicacion', 1, rutaTrabajadorServicio);
        try {
            const urlTrabajadorServicio = Base.construirUrlAbsoluta(rutaTrabajadorServicio);
            const instaladorAplicacion = new InstaladorAplicacion(this.gestorEstado, this.interfazUsuario, this.rutaErrores);
            await instaladorAplicacion.inicializarTrabajadorServicio(urlTrabajadorServicio);
            instaladorAplicacion.inicializarInstalacion();
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    async activarNotificaciones() {
        Base.trazarFlujo(this.constructor.name, 'activarNotificaciones', 1);
        try {
            const instaladorAplicacion = new InstaladorAplicacion(this.gestorEstado, this.interfazUsuario, this.rutaErrores);
            instaladorAplicacion.inicializarSuscripcion();
        } catch (error) {
            this.informarErrorModulo(this.manejadorErrores.procesarError(error));
        }
    }
    // Funciones para implementar "acciones" y "reacciones"
    noReaccionar() { return false; }
    //... + Extensiones
}

/* CLASE: OperadorDatos [singleton] (extensible)
PROPOSITO: Gestionar y manipular las operaciones y datos en la aplicación, actuando como un intermediario entre la lógica de negocio y las fuentes de datos, ya sean internas (como el estado de la aplicación) o externas (APIs y servicios de backend).
RESPONSABILIDADES:
1. Operaciones de Datos: Realiza operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y otras manipulaciones de datos necesarias para el funcionamiento de la aplicación.
2. Comunicación con APIs: Gestiona la comunicación con servicios externos y APIs, asegurando el envío y la recepción adecuada de datos.
3. Transformación de Datos: Convierte los datos recibidos de las APIs en formatos utilizables por la aplicación y viceversa.
4. Validación de Datos: Asegura la integridad y validez de los datos antes de su procesamiento o envío a servicios externos.
5. Manejo de Estado del Modelo: Mantiene el estado local de los datos, proporcionando un punto de acceso centralizado para su consulta y actualización, y publicando "eventos de Modelo" para notificar y/o encadenar cambios.
NOTAS: Esta clase es ampliable mediante la inyección de extensiones, a través de la configuración dinámica que se aplica al ejecutar cada servicio. Las funciones que se pueden agregar para ampliar la funcionalidad de esta clase se dividen en dos tipos principales:
- Funciones para implementar reacciones a eventos (tanto de la Vista como del propio Modelo).
- Operaciones de Datos, similares a "efectuarOperacion".
*/
class OperadorDatos { //(MODELO)
    constructor(validadorDatos=null) {
        this.validadorDatos = validadorDatos || new ValidadorDatos();
        this.comunicadorApi = null;
        this.gestorEstado = null;
        this.manejadorErrores = null;
        this.OPERACIONES = {};
    }
    static obtenerInstancia(validadorDatos=null) {
        if (!this.instancia) {
            this.instancia = new OperadorDatos(validadorDatos);
        }
        return this.instancia;
    }
    // Funciones privadas
    _asignarUidRecurso(uid, recurso) {
        if (uid && uid !== '') {
            if (recurso.includes('<uid>')) {
                recurso = recurso.replace('<uid>', uid);
            } else {
                recurso += `/${uid}`;
            }
        }
        return recurso;
    }
    // Funciones para configuración dinámica
    inyectarExtensiones(extensiones) {
        for (let nombreFuncion in extensiones) {
            if (extensiones.hasOwnProperty(nombreFuncion)) {
                let funcion = extensiones[nombreFuncion];
                if (typeof funcion === 'function') {
                    this[nombreFuncion] = funcion.bind(this);
                }
            }
        }
    }
    coordinarInicio(gestorEstado, manejadorErrores) {
        Base.trazarFlujo(this.constructor.name, 'coordinarInicio', 1);
        if (typeof gestorEstado === 'object' && typeof manejadorErrores === 'object') {
            this.gestorEstado = gestorEstado;
            this.manejadorErrores = manejadorErrores;
            this.comunicadorApi = new ComunicadorApi(this.gestorEstado);
        }
    }
    configurarOperaciones(declaracionesOperaciones) {
        Base.trazarFlujo(this.constructor.name, 'configurarOperaciones', 1);
        try {
            for (let operacion in declaracionesOperaciones) {
                if (declaracionesOperaciones.hasOwnProperty(operacion)) {
                    const config = declaracionesOperaciones[operacion];
                    this.OPERACIONES[operacion] = {
                        nombre: operacion,
                        metodo: config.metodo,
                        eventoExito: config.eventoExito,
                        eventoError: config.eventoError,
                        uidApi: config.uidApi,
                        limiteTiempo: config.limiteTiempo
                    };
                }
            }
        } catch (error) {
            throw error;
        }
    }
    async seleccionarServicioApi(uidApi) {
        Base.trazarFlujo(this.constructor.name, 'seleccionarServicioApi', 1, `uidApi=${uidApi}`);
        try {
            const estadosModelo = this.gestorEstado.obtenerEstado(Base.Estados.modelo);
            const serviciosApi = estadosModelo.get('serviciosApi');
            if (serviciosApi && serviciosApi[uidApi]) {
                const { urlApi, keyApi } = serviciosApi[uidApi];
                await this.comunicadorApi.configurarApi(uidApi, urlApi, keyApi);
            }
        } catch (error) {
            throw error;
        }
    }
    // Funciones para operaciones de datos
    async efectuarOperacion(portadorInformacion) {
        Base.trazarFlujo(this.constructor.name, 'efectuarOperacion', 1);
        let eventoErrorOperacion = '';
        let contextoOperacion = {};
        try {
            let { operacion, recurso, uid, valores, parametros } = portadorInformacion.recuperarInformacion('peticion');
            recurso = this._asignarUidRecurso(uid, recurso);
            let { metodo, eventoExito, eventoError, limiteTiempo, uidApi } = this.OPERACIONES[operacion];
            eventoErrorOperacion = eventoError;
            contextoOperacion = { operacion, metodo, recurso, uid };
            await this.seleccionarServicioApi(uidApi);
            const respuesta = await this.comunicadorApi.realizarPeticionApi(recurso, metodo, valores, parametros, limiteTiempo);
            let entrega = this.comunicadorApi.adaptarRespuestaApi(respuesta);
            portadorInformacion.almacenarInformacion(entrega);
            this.gestorEstado.emitirEventoInformacion(eventoExito, portadorInformacion.recuperarInformacion());
        } catch (error) {
            const errorProcesado = this.manejadorErrores.procesarError(error, contextoOperacion);
            this.gestorEstado.emitirEventoInformacion(eventoErrorOperacion, errorProcesado);
        }
    }
    comprobarDatosEnviados(portadorInformacion) {
        Base.trazarFlujo(this.constructor.name, 'comprobarDatosEnviados', 1);
        try {
            if (!portadorInformacion.FORMULARIO || !portadorInformacion.peticion['valores']) { return false; }
            const { estado, errores } = this.validadorDatos.evaluarFormulario(
                portadorInformacion.peticion['valores'], portadorInformacion.FORMULARIO
            );
            if (!estado && errores) {
                portadorInformacion.asignarErrores(errores);
                this.gestorEstado.emitirEventoInformacion('ERROR_COMPROBACION_DATOS', portadorInformacion.recuperarInformacion());
                return false;
            }
            return true;
        } catch (error) {
            throw error;
        }
    }
    // Funciones para implementar reacciones a eventos y operaciones de datos
    noReaccionar() { return false; }
    //... + Extensiones
}

/* CLASE: InterfazUsuario [singleton] (extensible)
PROPOSITO: Manejar la interfaz gráfica, la presentación audiovisual y la interacción del usuario con la aplicación, proporcionando un punto de contacto entre el usuario y las funcionalidades de la aplicación para asegurar una experiencia de uso fluida, comprensible y coherente.
RESPONSABILIDADES:
1. Renderizado de UI: Controla la presentación visual de elementos de la interfaz, como formularios, listas y mensajes.
2. Manejo de Eventos: Gestiona eventos de usuario (clicks, entradas de teclado, etc.) y los enlaza con interacciones correspondientes en la aplicación.
3. Comunicación con otros Componentes: Actúa como intermediario entre el usuario y otros componentes del sistema, a través del CoordinadorGeneral.
4. Actualización Dinámica de UI: Actualiza la interfaz en respuesta a cambios de estado en la aplicación, asegurando que los datos mostrados estén siempre actualizados.
5. Manejo de Estado de la Vista: Mantiene el estado de la vista, proporcionando un punto de acceso centralizado para su consulta y actualización, y publicando "eventos de Vista" para notificar y/o encadenar cambios.
NOTAS: Esta clase es ampliable mediante la inyección de extensiones, a través de la configuración dinámica que se aplica al ejecutar cada servicio. Las funciones que se pueden agregar para ampliar la funcionalidad de esta clase se dividen en dos tipos principales:
- Funciones para implementar reacciones a eventos (tanto eventos del Modelo como de la propia Vista).
- Manejadores de interacciones de UI (manejadoresInteracciones).
- Controladores de "objetos de datos" de la UI.
- Controladores de "objetos de interacción" de la UI.
*/
class InterfazUsuario { //(VISTA)
    constructor(frameworkFrontend, traductorIdiomas=null, receptorUI=null, manipuladorUI=null, presentadorContenido=null) {
        this.ELEMENTOS = new Map();
        this.EVENTOS = new Map();
        this.MANEJADORES = new Map();
        this.PLANTILLAS = new Map();
        this.adaptadorUI = new AdaptadorUI(frameworkFrontend);
        this.receptorUI = receptorUI || new ReceptorUI();
        this.manipuladorUI = manipuladorUI || new ManipuladorUI();
        this.traductorIdiomas = traductorIdiomas || new TraductorIdiomas();
        this.presentadorContenido = presentadorContenido || new PresentadorContenido();
        this.gestorEstado = null;
        this.manejadorErrores = null;
        this.timeoutVisor = null;
    }
    static obtenerInstancia(frameworkFrontend, traductorIdiomas=null, receptorUI=null, manipuladorUI=null, presentadorContenido=null) {
        if (!this.instancia) {
            this.instancia = new InterfazUsuario(frameworkFrontend, traductorIdiomas, receptorUI, manipuladorUI, presentadorContenido);
        }
        return this.instancia;
    }
    // Funciones privadas
    _asignarEventosAcciones() {
        const acciones = this.manipuladorUI.seleccionar('.accion', 'todos');
        acciones.forEach(accion => {
            const evento = this.EVENTOS.get(accion.id);
            if (evento) {
                this.receptorUI.gestionarOyenteEvento(
                    'asignar', accion, evento.tipo, evento.manejador
                );
            }
        });
    }
    _eliminarEventosAcciones() {
        const acciones = this.manipuladorUI.seleccionar('.accion', 'todos');
        acciones.forEach(accion => {
            const evento = this.EVENTOS.get(accion.id);
            if (evento) {
                this.receptorUI.gestionarOyenteEvento(
                    'eliminar', accion, evento.tipo, evento.manejador
                );
            }
        });
    }
    // Funciones de configuración dinámica
    inyectarExtensiones(extensiones) {
        for (let nombreFuncion in extensiones) {
            if (extensiones.hasOwnProperty(nombreFuncion)) {
                let funcion = extensiones[nombreFuncion];
                if (typeof funcion === 'function') {
                    this[nombreFuncion] = funcion.bind(this);
                }
            }
        }
    }
    coordinarInicio(gestorEstado, manejadorErrores) {
        Base.trazarFlujo(this.constructor.name, 'coordinarInicio', 1);
        if (typeof gestorEstado === 'object' && typeof manejadorErrores === 'object') {
            this.gestorEstado = gestorEstado;
            this.manejadorErrores = manejadorErrores;
            this.presentadorContenido.asignarMapaPlantillas(this.PLANTILLAS);
            this.ELEMENTOS.set('visorMensajes', this.manipuladorUI.seleccionar('#visorMensajes'));
            this.ELEMENTOS.set('ventanaModal', this.manipuladorUI.seleccionar('#ventanaModal'));
        }
    }
    // Funciones de alto nivel para "objetos de interacción" de UI
    abrirVentanaModal(contenido, selector='ventanaModal', callback=null) {
        // Depende de Bootstrap
        Base.trazarFlujo(this.constructor.name, 'abrirVentanaModal', 1, selector);
        const ventana = this.ELEMENTOS.get(selector);
        if (!ventana) return;
        contenido = this.presentadorContenido.representarContenido(
            'plantillaModal', { 'contenido_modal': contenido }
        );
        contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
        this.manipuladorUI.actualizarContenido(ventana, contenido);
        let modal = this.adaptadorUI.obtenerComponente('Modal', ventana);
        if (typeof callback === 'function') {
            this.receptorUI.gestionarOyenteEvento(
                'asignar', ventana, 'shown.bs.modal', callback, { once: true }
            );
        }
        if (!this.manipuladorUI.elementoContieneClase('modal-open')) {
            modal.show();
            this._asignarEventosAcciones();
        }
    }
    cerrarVentanaModal(selector='ventanaModal') {
        // Depende de Bootstrap
        Base.trazarFlujo(this.constructor.name, 'cerrarVentanaModal', 1, selector);
        const ventana = this.ELEMENTOS.get(selector);
        if (!ventana) return;
        let modal = this.adaptadorUI.obtenerComponente('Modal', ventana);
        if (!modal || !this.manipuladorUI.elementoContieneClase('modal-open')) return;
        modal.hide();
        this.receptorUI.gestionarOyenteEvento(
            'asignar', ventana, 'hidden.bs.modal', () => {
                this._eliminarEventosAcciones();
                this.manipuladorUI.actualizarContenido(ventana, '');
            }, { once: true }
        );
    }
    mostrarInformacion(mensaje, tipo='success', selector='visorMensajes') {
        Base.trazarFlujo(this.constructor.name, 'mostrarInformacion', 1, selector, `tipo=${tipo}`);
        const elemento = this.ELEMENTOS.get(selector);
        if (elemento) {
            this.manipuladorUI.manejarClasesElemento('quitar', 'alert-success,alert-warning,alert-danger,alert-info', elemento);
            this.manipuladorUI.manejarClasesElemento('agregar', `alert-${tipo}`, elemento);
            const marcadores = this.presentadorContenido.separarTextoEnPartes(mensaje);
            let contenido = this.presentadorContenido.representarMensaje(marcadores);
            contenido = this.traductorIdiomas.aplicarTraduccion(contenido);
            this.manipuladorUI.actualizarContenido(elemento, contenido);
            this.manipuladorUI.cambiarVisibilidad(elemento, true, true);
            const tiempoVisor = this.gestorEstado.leerPreferenciaUsuario('tiempoVisor', 10);
            if (this.timeoutVisor) {
                clearTimeout(this.timeoutVisor);
            }
            this.timeoutVisor = setTimeout( () => {
                this.manipuladorUI.cambiarVisibilidad(elemento, false, true);
                this.timeoutVisor = null;
            }, tiempoVisor * 1000);
        }
    }
    alternarPaneles(ocultar, mostrar) {
        Base.trazarFlujo(this.constructor.name, 'alternarPaneles', 1, `ocultar=${ocultar}`, `mostrar=${mostrar}`);
        const aparecer = this.ELEMENTOS.get(mostrar);
        const desaparecer = this.ELEMENTOS.get(ocultar);
        if (desaparecer) {
            this.manipuladorUI.animarElemento(desaparecer, 'fadeOut');
            this.receptorUI.gestionarOyenteEvento(
                'asignar', desaparecer, 'transitionend', () => {
                    if (aparecer) {
                        this.manipuladorUI.animarElemento(aparecer, 'fadeIn');
                    }
                }, { once: true }
            );
        } else {
            this.manipuladorUI.animarElemento(aparecer, 'fadeIn');
        }
    }
    cerrarMenusAbiertos() {
        Base.trazarFlujo(this.constructor.name, 'cerrarMenusAbiertos', 1);
        const collapses = this.manipuladorUI.seleccionar('.navbar-collapse, .menu_opciones', 'todos');
        collapses.forEach(collapse => {
            let collapseInstance = this.adaptadorUI.crearComponente(
                'Collapse', collapse, {toggle: false}
            );
            collapseInstance.hide();
        });
    }
    alternarEsperando(visible=true, selector='area_cuerpo') {
        Base.trazarFlujo(this.constructor.name, 'alternarEsperando', 1, `visible=${visible}`, selector);
        const area = this.ELEMENTOS.get('area_esperando');
        const elemento = this.ELEMENTOS.get(selector);
        if (area) {
            this.manipuladorUI.cambiarVisibilidad(area, visible);
        }
        if (elemento) {
            this.manipuladorUI.cambiarVisibilidad(elemento, !visible);
        }
    }
    abrirUrl(url, destino='') {
        Base.trazarFlujo(this.constructor.name, 'abrirUrl', 1, `url=${url}`, `destino=${destino}`);
        if (!/^https?:\/\//i.test(url)) {
            url = `https://${url}`;
        }
        destino ? window.open(url, destino) : window.location.href = url;
    }
    activarTextosEmergentes(selector) {
        // Depende de Bootstrap
        Base.trazarFlujo(this.constructor.name, 'activarTextosEmergentes', 1, selector);
        const elemento = this.manipuladorUI.seleccionar(selector);
        let tooltipTriggerList = [].slice.call(elemento.querySelectorAll('[data-bs-toggle="tooltip"]'))
        let tooltipList = tooltipTriggerList.map( (tooltipTriggerEl) => {
          return this.adaptadorUI.crearComponente('Tooltip', tooltipTriggerEl);
        });
    }
    enrutarInteraccion(selectorContenedor, mapeoAcciones, evento) {
        Base.trazarFlujo(this.constructor.name, 'enrutarInteraccion', 1, selectorContenedor);
        Object.keys(mapeoAcciones).forEach(claseAccion => {
            if (evento.target.classList.contains(claseAccion)) {
                const elemento = evento.target.closest(selectorContenedor);
                const contexto = this.receptorUI.capturarDatosContexto(elemento);
                mapeoAcciones[claseAccion].call(this, contexto);
            }
        });
    }
    // Funciones para implementar reacciones a eventos, controladores de objetos de UI + manejadores de interacciones.
    noReaccionar() { return false; }
    reaccionEnviandoPeticion() { return false; }
    reaccionRespuestaRecibida() { return false; }
    //... + Extensiones (manejadoresInteracciones)
    //... + Extensiones (interfazUsuario)
}

/* **************************************************************************** */
/* CLASES COMPLEMENTARIAS DEL AMBITO DE LA "VISTA" */

/* CLASE: PresentadorContenido (extensible)
PROPOSITO: Proporcionar herramientas y utilidades para convertir, formatear y preparar la presentación de contenidos en la interfaz de usuario (UI), empleando plantillas para transformarlos en representaciones visuales adecuadas.
RESPONSABILIDADES:
1. Procesa y adapta los datos y esquemas para su presentación en la UI, asegurando que se muestren de manera comprensible y accesible para los usuarios.
2. Aplica plantillas de diseño para la generación dinámica de contenidos en los diferentes componentes de datos de la UI (paneles, formularios, informes, etc.), personalizando su visualización según las necesidades y permisos del usuario.
3. Realiza sustituciones y reemplazos en las plantillas basadas en los datos proporcionados, permitiendo una presentación dinámica y contextual de la información.
NOTAS:
Depende directamente de los esquemas proporcionados por "ProcesadorEsquemas", ya que estos definen la estructura y el formato de los datos a presentar.
Interactúa con la clase "TraductorIdiomas" para aplicar traducciones y adaptaciones regionales en la presentación de los datos.
*/
class PresentadorContenido {
    constructor() {
        this.plantillas = null;
    }
    // Funciones de configuración dinámica
    inyectarExtensiones(extensiones) {
        //Base.trazarFlujo(this.constructor.name, 'inyectarExtensiones', 2);
        for (let nombreFuncion in extensiones) {
            if (extensiones.hasOwnProperty(nombreFuncion)) {
                let funcion = extensiones[nombreFuncion];
                if (typeof funcion === 'function') {
                    this[nombreFuncion] = funcion.bind(this);
                }
            }
        }
    }
    // Funciones para modificar contenidos
    convertirUrlAEnlaces(contenido) {
        Base.trazarFlujo(this.constructor.name, 'convertirUrlAEnlaces', 3);
        const regex = /(https?:\/\/\S+)/gi;
        return contenido.replace(regex, '<a href="$1" target="_blank" class="enlace-url">$1</a>');
    }
    sustituirClaves(contenido, claves) {
        Base.trazarFlujo(this.constructor.name, 'sustituirClaves', 3);
        return contenido.replace(/{{(.*?)}}/g, (match) => {
            return claves[match.split(/{{|}}/).filter(Boolean)[0].trim()]
        });
    }
    sustituirFechaHora(contenido) {
        Base.trazarFlujo(this.constructor.name, 'sustituirFechaHora', 3);
        const fechas = Base.formatosDeFecha();
        let marcadores = {};
        for (let clave in fechas) {
            if (fechas[clave]) {
                marcadores[`fechahora_${clave}`] = fechas[clave];
            }
        }
        contenido = Base.reemplazarMarcadores(contenido, marcadores);
        return contenido;
    }
    separarTextoEnPartes(texto, separador='|') {
        Base.trazarFlujo(this.constructor.name, 'separarTextoEnPartes', 3);
        if (String(texto).includes(separador)) {
            let partes = ['', '', ''];
            partes = texto.split(separador);
            while (partes.length < 3) {
                partes.push('');
            }
            let [ titulo, contenido, descripcion ] = partes;
            return { "titulo": titulo, "contenido": contenido, "descripcion": descripcion };
        } else {
            return { "titulo": '', "contenido": texto, "descripcion": '' };
        }
    }
    reemplazarDatos(contenido, datos) {
        Base.trazarFlujo(this.constructor.name, 'reemplazarDatos', 3);
        let marcadores = {};
        for (let clave in datos) {
            for (let campo in datos[clave]) {
                const valor = datos[clave][campo];
                if (valor && typeof valor !== 'object') {
                    marcadores[`${clave}_${campo}`] = valor;
                }
            }
        }
        contenido = Base.reemplazarMarcadores(contenido, marcadores);
        return contenido;
    }
    // Funciones para gestionar plantillas HTML
    asignarMapaPlantillas(mapaPlantillas) {
        Base.trazarFlujo(this.constructor.name, 'asignarMapaPlantillas', 3);
        this.plantillas = mapaPlantillas;
    }
    agregarPlantillasContenedor(contenido, contenedor, reemplazar=false) {
        Base.trazarFlujo(this.constructor.name, 'agregarPlantillasContenedor', 3, contenedor, `reemplazar=${reemplazar}`);
        const contenedorPlantillas = document.getElementById(contenedor);
        if (!contenido || !contenedorPlantillas) return;
        const contenedorTemporal = document.createElement('div');
        contenedorTemporal.innerHTML = contenido;
        // Función para procesar cada plantilla individual
        const procesarPlantilla = plantilla => {
            const plantillaExistente = contenedorPlantillas.querySelector(`#${plantilla.id}`);
            if (plantillaExistente) {
                plantillaExistente.innerHTML = plantilla.innerHTML;
            } else {
                contenedorPlantillas.appendChild(plantilla);
            }
        };
        // Iterar sobre las plantillas cargadas en el contenedor temporal
        Array.from(contenedorTemporal.children).forEach(plantilla => {
            procesarPlantilla(plantilla);
        });
        if (reemplazar) {
            contenedorPlantillas.innerHTML = '';
            contenedorPlantillas.appendChild(contenedorTemporal);
        }
    }
    autoregistrarPlantillas(contenedor) {
        Base.trazarFlujo(this.constructor.name, 'autoregistrarPlantillas', 3);
        this.plantillas.clear();
        const contenedorPlantillas = document.getElementById(contenedor);
        if (contenedorPlantillas) {
            const plantillas = contenedorPlantillas.children;
            Array.from(plantillas).forEach(plantilla => {
                if (plantilla.tagName === 'DIV' && plantilla.id) {
                    this.plantillas.set(plantilla.id, plantilla);
                }
            });
        }
    }
    // Procesadores para analizar y representar plantillas HTML (Template Parser + Rendering)
    representarMensaje(marcadores) {
        Base.trazarFlujo(this.constructor.name, 'representarMensaje', 2);
        let contenido = '<div class="mensaje-titulo">((titulo))</div><div class="mensaje-contenido">((contenido))</div><div class="mensaje-descripcion">((descripcion))</div>';
        contenido = Base.reemplazarMarcadores(contenido, marcadores);
        return contenido;
    }
    representarContenido(plantilla, marcadores) {
        Base.trazarFlujo(this.constructor.name, 'representarContenido', 2, plantilla);
        let contenido = '';
        if (this.plantillas.has(plantilla)) {
            const elemento = this.plantillas.get(plantilla);
            if (elemento) {
                contenido = elemento.innerHTML;
                contenido = Base.reemplazarMarcadores(contenido, marcadores);
            }
        }
        return contenido;
    }
}

/* CLASE: ReceptorUI
PROPOSITO: Gestionar la captura y transferencia de las entradas del usuario desde la UI, interactuando directamente con sus componentes para recopilar y procesar los datos ingresados.
RESPONSABILIDADES:
1. Extrae datos de los campos de formularios en la UI, como campos de texto, checkboxes, radios, etc.
2. Facilita la obtención de valores, contenidos y estados desde diferentes elementos de la UI.
3. Ofrece una interfaz estandarizada para la recopilación de datos de la UI, independientemente del tipo o la estructura de los componentes de entrada.
NOTAS:
Requiere un acceso directo a los elementos del DOM (Document Object Model) para poder recopilar los datos.
Trabaja en conjunto con la clase "InterfazUsuario" para garantizar que los datos recogidos se integren de manera coherente en el flujo general de la aplicación.
*/
class ReceptorUI {
    obtenerDatosFormulario(selector) {
        Base.trazarFlujo(this.constructor.name, 'obtenerDatosFormulario', 2, selector);
        let datosFormulario = {};
        let checkboxesProcesados = {};
        const formulario = document.getElementById(selector);
        if (!formulario) {
            return datosFormulario;
        }
        const formData = new FormData(formulario);
        for (let [clave, valor] of formData.entries()) {
            if (formulario[clave].type === "checkbox") {
                if (!checkboxesProcesados[clave]) {
                    datosFormulario[clave] = [];
                    checkboxesProcesados[clave] = true;
                    document.querySelectorAll(`input[type="checkbox"][name="${clave}"]:checked`).forEach((checkbox) => {
                        datosFormulario[clave].push(checkbox.value);
                    });
                }
            } else {
                datosFormulario[clave] = valor;
            }
        }
        return datosFormulario;
    }
    obtenerValorElemento(selector) {
        Base.trazarFlujo(this.constructor.name, 'obtenerValorElemento', 2, selector);
        const elemento = document.getElementById(selector);
        if (!elemento) return '';
        switch (elemento.type) {
            case 'checkbox':
                return elemento.checked;
            case 'radio':
                let radioSeleccionado = document.querySelector(`input[name="${elemento.name}"]:checked`);
                return radioSeleccionado ? radioSeleccionado.value : '';
            default:
                return elemento.value;
        }
    }
    obtenerValorCampo(idFormulario, nombreCampo) {
        Base.trazarFlujo(this.constructor.name, 'obtenerValorCampo', 2, `form=${idFormulario}`, `campo=${nombreCampo}`);
        const formulario = document.getElementById(idFormulario);
        if (!formulario) return;
        const selector = `[name="${nombreCampo}"]`;
        const elemento = formulario.querySelector(selector);
        if (!elemento) return;
        switch (elemento.type) {
            case 'checkbox':
                return elemento.checked;
            case 'radio':
                let radioSeleccionado = document.querySelector(`input[name="${elemento.name}"]:checked`);
                return radioSeleccionado ? radioSeleccionado.value : '';
            default:
                return elemento.value;
        }
    }
    obtenerTextoElemento(selector) {
        Base.trazarFlujo(this.constructor.name, 'obtenerTextoElemento', 2, selector);
        const elemento = document.getElementById(selector);
        if (!elemento) return '';
        let contenido = elemento.textContent;
        contenido = contenido.replace(/^\s+/gm, '').replace(/\s{2,}/g, ' ').replace(/\n\s*\n/g, '\n');
        return contenido;
    }
    capturarDatosContexto(elemento) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'capturarDatosContexto', 2, idElemento);
        if (!elemento) return {};
        let datos = {};
        for (const clave in elemento.dataset) {
            if (elemento.dataset.hasOwnProperty(clave)) {
                datos[clave] = elemento.dataset[clave];
            }
        }
        return datos;
    }
    gestionarOyenteEvento(opcion, elemento, evento, manejador, opciones={}) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'gestionarOyenteEvento', 3, opcion, evento, idElemento);
        if (elemento) {
            if (opcion==='asignar') {
                elemento.addEventListener(evento, manejador, opciones);
            } else {
                elemento.removeEventListener(evento, manejador);
            }
        }
    }
}

/* CLASE: ManipuladorUI
PROPOSITO: Gestionar las manipulaciones directas de los componentes dinámicos de la UI, los efectos visuales de la vista y las actualizaciones de sus datos y contenidos.
RESPONSABILIDADES:
1. Realiza cambios visuales en la interfaz, como mostrar u ocultar elementos, aplicar animaciones y transiciones, redimensionar elementos y realizar ajustes de estilo.
2. Proporciona un conjunto de herramientas para simplificar la manipulación de elementos del DOM (Document Object Model), abstrayendo su complejidad.
3. Actualiza los datos y contenidos en la UI, en respuesta a acciones del usuario o cambios en el estado de la aplicación.
NOTAS:
Requiere un acceso directo a los elementos del DOM (Document Object Model) para poder realizar sus funciones.
Trabaja en conjunto con la clase "InterfazUsuario" para asegurar que las manipulaciones efectuadas se reflejen y sincronicen en la UI.
*/
class ManipuladorUI {
    asignarTextoElemento(selector, texto='') {
        Base.trazarFlujo(this.constructor.name, 'asignarTextoElemento', 2, selector);
        const elemento = document.getElementById(selector);
        if (!elemento) return;
        elemento.textContent = texto;
    }
    asignarValorCampo(idFormulario, nombreCampo, valor='') {
        Base.trazarFlujo(this.constructor.name, 'asignarValorCampo', 2, `form=${idFormulario}`, `${nombreCampo}=${valor}`);
        const formulario = document.getElementById(idFormulario);
        if (!formulario) return;
        const selector = `[name="${nombreCampo}"]`;
        const elemento = formulario.querySelector(selector);
        if (!elemento) return;
        switch (elemento.type) {
            case 'checkbox':
                elemento.checked = valor;
                break;
            case 'radio':
                const radios = formulario.querySelectorAll(`input[name="${nombreCampo}"]`);
                radios.forEach((radio) => {
                    if (radio.value === valor) radio.checked = true;
                });
                break;
            default:
                elemento.value = valor;
        }
    }
    cambiarTamanoFuente(opcion='+', selector='.fuente-ajustable') {
        Base.trazarFlujo(this.constructor.name, 'cambiarTamanoFuente', 2, opcion, selector);
        const tamanoMaximo = 3;
        const tamanoMinimo = 0.25;
        const elementos = document.querySelectorAll(selector);
        const tamanoBaseFuente = parseFloat(getComputedStyle(document.documentElement).fontSize);
        elementos.forEach(elemento => {
            let fontSize = parseFloat(getComputedStyle(elemento).fontSize) / tamanoBaseFuente;
            if (opcion === '+') {
                fontSize += 0.1;
            } else if (opcion === '-') {
                fontSize -= 0.1;
            }
            fontSize = Math.max(tamanoMinimo, Math.min(fontSize, tamanoMaximo));
            elemento.style.fontSize = `${fontSize}rem`;
        });
    }
    copiarContenido(contenido) {
        Base.trazarFlujo(this.constructor.name, 'copiarContenido', 2);
        if (!contenido || contenido === '') return false;
        let auxiliar = document.createElement('textarea');
        auxiliar.value = contenido;
        document.body.appendChild(auxiliar);
        auxiliar.select();
        try {
            document.execCommand('copy');
        } catch (error) {
            return false;
        }
        document.body.removeChild(auxiliar);
        return true;
    }
    ajustarAlturaCampo(selector, maximo=400) {
        Base.trazarFlujo(this.constructor.name, 'ajustarAlturaCampo', 2, selector, maximo);
        const elemento = document.getElementById(selector);
        if (elemento) {
            const scrollHeightActual = elemento.scrollHeight;
            elemento.style.height = 'auto';
            elemento.style.height = `${scrollHeightActual}px`;
            const maxHeight = maximo;
            if (scrollHeightActual > maxHeight) {
                elemento.style.height = `${maxHeight}px`;
                elemento.style.overflowY = 'auto';
            } else {
                elemento.style.overflowY = 'hidden';
            }
            if (elemento.value.length === 0) {
                elemento.style.height = 'auto';
            }
        }
    }
    resaltarPalabrasEnTextos(texto, selector) {
        Base.trazarFlujo(this.constructor.name, 'resaltarPalabrasEnTextos', 2, selector);
        const palabras = texto.split(/\s+/).filter(palabra => palabra.length >= 4);
        if (palabras.length === 0) return;
        const palabrasEscapadas = palabras.map(palabra => palabra.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        const regex = new RegExp(`\\b(${palabrasEscapadas.join('|')})\\b`, 'gi');
        document.querySelectorAll(`.${selector}`).forEach(elemento => {
            elemento.innerHTML = elemento.textContent.replace(regex, '<b>$&</b>');
        });
    }
    seleccionar(selector, cuantos='uno') {
        Base.trazarFlujo(this.constructor.name, 'seleccionar', 3, selector, cuantos);
        if (cuantos==='uno') {
            return document.querySelector(selector);
        } else {
            return document.querySelectorAll(selector);
        }
    }
    animarElemento(elemento, efecto='fadeIn') {
        // Depende de Bootstrap
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'animarElemento', 3, idElemento, efecto);
        if (!elemento) return;
        if (!elemento.classList.contains('fade')) {
            elemento.classList.add('fade');
        }
        if (efecto === 'fadeIn') {
            elemento.style.display = 'block';
            setTimeout(() => elemento.classList.add('show'), 10);
        } else if (efecto === 'fadeOut') {
            elemento.classList.remove('show');
            elemento.addEventListener('transitionend', function manejador() {
                elemento.style.display = 'none';
                elemento.removeEventListener('transitionend', manejador);
            }, { once: true });
        }
    }
    cambiarVisibilidad(elemento, visible=true, animar=false) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'cambiarVisibilidad', 2, idElemento, `visible=${visible}`, `animar=${animar}`);
        if (!elemento) return;
        if (!elemento.classList.contains('fade')) {
            elemento.classList.add('fade');
        }
        if (animar) {
            if (visible) {
                this.animarElemento(elemento, 'fadeIn');
            } else {
                this.animarElemento(elemento, 'fadeOut');
            }
        } else {
            if (visible) {
                elemento.style.display = 'block';
                elemento.classList.add('show');
            } else {
                elemento.style.display = 'none';
                elemento.classList.remove('show');
            }
        }
    }
    actualizarContenido(elemento, contenido) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'actualizarContenido', 2, idElemento);
        if (elemento) {
            elemento.innerHTML = contenido;
        }
    }
    resaltarElemento(elemento, resaltado=true) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'resaltarElemento', 2, idElemento, resaltado);
        if (elemento) {
            if (resaltado) {
                elemento.classList.add('mark');
            } else {
                elemento.classList.remove('mark');
            }
        }
    }
    resaltarSeleccionados(selector, resaltar=true) {
        Base.trazarFlujo(this.constructor.name, 'resaltarSeleccionados', 2, selector, resaltar);
        document.querySelectorAll(selector).forEach(elemento => {
            if (resaltar) {
                elemento.classList.add('mark');
            } else {
                elemento.classList.remove('mark');
            }
        });
    }
    manejarClasesElemento(opcion, clases, elemento) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'manejarClasesElemento', 3, opcion, clases, idElemento);
        if (elemento) {
            const listaDeClases = clases.split(',');
            listaDeClases.forEach(clase => {
                elemento.classList.remove(clase.trim());
                if (opcion === 'agregar') {
                    elemento.classList.add(clase.trim());
                }
            });
        }
    }
    elementoContieneClase(clase, elemento) {
        Base.trazarFlujo(this.constructor.name, 'elementoContieneClase', 3, clase);
        if(!elemento) {
            elemento = document.body;
        }
        return elemento.classList.contains(clase);
    }
    enfocarEnCampo(idFormulario, nombreCampo) {
        Base.trazarFlujo(this.constructor.name, 'enfocarEnCampo', 2, `form=${idFormulario}`, `campo=${nombreCampo}`);
        const formulario = document.getElementById(idFormulario);
        if (!formulario) return;
        const selector = `[name="${nombreCampo}"]`;
        const elemento = formulario.querySelector(selector);
        if (!elemento) return;
        elemento.focus();
    }
    enfocarEnSeleccion(selector) {
        Base.trazarFlujo(this.constructor.name, 'enfocarEnSeleccion', 2, selector);
        const elemento = document.getElementById(selector);
        if (elemento) {
            elemento.focus();
        }
    }
    desplazarHaciaSeleccion(selector) {
        Base.trazarFlujo(this.constructor.name, 'desplazarHaciaSeleccion', 3, selector);
        const elemento = document.getElementById(selector);
        if (elemento) {
            if (elemento) {
                const posicionTop = elemento.getBoundingClientRect().top + window.pageYOffset;
                window.scrollTo({ top: posicionTop, behavior: 'smooth' });
            }
        }
    }
    configurarElemento(elemento, opciones=null, funcionOyente=null) {
        const idElemento = (elemento.id || '');
        Base.trazarFlujo(this.constructor.name, 'configurarElemento', 2, idElemento, opciones);
        if (!elemento || !opciones) return;
        const elementoNuevo = elemento.cloneNode(true);
        elemento.parentNode.replaceChild(elementoNuevo, elemento);
        elemento = elementoNuevo;
        const { visible=true, activado, etiqueta='', clase='' } = opciones;
        elemento.style.display = visible ? 'block' : 'none';
        if (typeof activado !== 'undefined') {
            elemento.disabled = !activado;
        }
        if (etiqueta) {
            elemento.textContent = etiqueta;
        }
        if (clase) {
            elemento.classList.add(clase);
        }
        if (typeof funcionOyente === 'function') {
            elemento.addEventListener('click', funcionOyente);
        }
    }
}

/* CLASE: TraductorIdiomas
PROPOSITO: Gestionar la internacionalización y localización en las aplicaciones web, proporcionando un mecanismo para cambiar y administrar los textos traducidos a diferentes idiomas en la interfaz de usuario (UI).
RESPONSABILIDADES:
1. Carga y aplica diferentes conjuntos de traducciones, permitiendo a los usuarios interactuar con la aplicación en su idioma preferido.
2. Provee funciones para cambiar el idioma seleccionado, traducir los textos de la UI y actualizar la vista dinámicamente.
3. Mantiene el estado del idioma actual, asegurando que todas las partes de la aplicación utilicen la misma configuración de internacionalización/localización.
NOTAS:
Depende de los archivos de idioma que contienen las traducciones de los textos de la UI en diferentes idiomas, en formato JSON.
Colabora con la clase "PresentadorContenido" para aplicar las traducciones y formatos regionales a los elementos de la UI.
*/
class TraductorIdiomas {
    constructor(idioma='es', textos=null) {
        this.idioma = idioma;
        if (!textos) {
            textos = Base.textosUI;
        }
        this.TEXTOS = new Map(Object.entries(textos));
        this.rutaIdioma = '';
    }
    asignarDesdeDatos(datos, idioma, limpiar=false) {
        Base.trazarFlujo(this.constructor.name, 'asignarDesdeDatos', 4, idioma, `limpiar=${limpiar}`);
        this.idioma = idioma || this.idioma;
        if (limpiar) {
            this.TEXTOS.clear();
        }
        Object.entries(datos).forEach(([clave, valor]) => this.TEXTOS.set(clave, valor));
    }
    async cargarDesdeJson(rutaIdioma, idiomaElegido, limpiar=false) {
        Base.trazarFlujo(this.constructor.name, 'cargarDesdeJson', 3, `idioma=${idiomaElegido}`, rutaIdioma);
        try {
            this.rutaIdioma = rutaIdioma;
            rutaIdioma = rutaIdioma.replace('[idioma]', idiomaElegido);
            const respuesta = await fetch(rutaIdioma);
            if (!respuesta.ok) {
                throw new ErrorPersonalizado('ERROR_CARGAR_IDIOMA', respuesta.statusText, {"ruta": rutaIdioma}, respuesta.status);
            }
            const datos = await respuesta.json();
            this.asignarDesdeDatos(datos.textosUI, datos.idioma, limpiar);
            return true;
        } catch (error) {
            throw error;
        }
    }
    async cambiarIdioma(idioma) {
        Base.trazarFlujo(this.constructor.name, 'cambiarIdioma', 2, `idioma=${idioma}`);
        try {
            await this.cargarDesdeJson(this.rutaIdioma, idioma);
        } catch (error) {
            throw error;
        }
    }
    aplicarTraduccion(contenido) {
        Base.trazarFlujo(this.constructor.name, 'aplicarTraduccion', 2);
        this.TEXTOS.forEach((valor, clave, map) => {
            contenido = contenido.replace(new RegExp(`\\(\\(${clave}\\)\\)`, 'g'), valor);
        });
        return contenido;
    }
    _(clave, predeterminado=clave) {
        Base.trazarFlujo(this.constructor.name, '_', 4, clave);
        return this.TEXTOS.get(clave) || predeterminado;
    }
}

/* CLASE: AdaptadorUI
PROPOSITO: Gestionar los componentes de diseño de la interfaz de usuario (UI), proporcionando una capa de abstracción sobre bibliotecas de front-end específicas (como Bootstrap) para facilitar la creación y uso de componentes de UI comunes (como modales, tooltips, toasts, etc.) de manera estandarizada y desacoplada del framework subyacente.
RESPONSABILIDADES:
1. Inyección y Gestión de Componentes UI: Inyecta y gestiona instancias de componentes de UI de bibliotecas de front-end. Esto incluye la inicialización y configuración de dichos componentes.
2. Interfaz Unificada para Componentes UI: Provee una interfaz sencilla y unificada para la creación y acceso a componentes de UI, simplificando su uso y evitando la dependencia directa del framework de front-end.
3. Registro y Obtención de Componentes: Facilita el registro y la obtención de componentes de UI, soportando la creación bajo demanda con configuración inicial básica. Esto permite a los desarrolladores obtener fácilmente instancias de componentes preconfigurados y listos para usar.
NOTAS:
Depende de las bibliotecas de front-end específicas que se utilicen en la aplicación, como Bootstrap, para la implementación real de los componentes de UI. Sin embargo, mantiene una separación clara entre la lógica de la aplicación y los detalles específicos de estas bibliotecas.
*/
class AdaptadorUI {
    constructor(frameworkFrontend) {
        this.frameworkFrontend = frameworkFrontend;
        this.COMPONENTES = {};
    }
    // Funciones privadas
    _manejarError(error, nombreComponente) {
        throw new ErrorPersonalizado('ERROR_COMPONENTE_UI', error.message, {"componente": nombreComponente});
    }
    // Funciones públicas
    registrarComponente(nombreComponente, elementosSeleccionados, configuracion) {
        Base.trazarFlujo(this.constructor.name, 'registrarComponente', 3, nombreComponente);
        try {
            if (!this.COMPONENTES[nombreComponente]) {
                this.COMPONENTES[nombreComponente] = this.crearComponente(nombreComponente, elementosSeleccionados, configuracion);
            }
        } catch (error) {
            this._manejarError(error, nombreComponente);
        }
    }
    obtenerComponente(nombreComponente, elementosSeleccionados) {
        Base.trazarFlujo(this.constructor.name, 'obtenerComponente', 3, nombreComponente);
        try {
            if (!this.COMPONENTES[nombreComponente]) {
                this.registrarComponente(nombreComponente, elementosSeleccionados);
            }
            return this.COMPONENTES[nombreComponente];
        } catch (error) {
            this._manejarError(error, nombreComponente);
        }
    }
    crearComponente(nombreComponente, elementosSeleccionados, configuracion) {
        Base.trazarFlujo(this.constructor.name, 'crearComponente', 3, nombreComponente);
        try {
            if (this.frameworkFrontend && this.frameworkFrontend[nombreComponente]) {
                return new this.frameworkFrontend[nombreComponente](elementosSeleccionados, configuracion);
            }
        } catch (error) {
            this._manejarError(error, nombreComponente);
        }
        return null;
    }
}

/* **************************************************************************** */
/* CLASES COMPLEMENTARIAS DEL AMBITO DEL "MODELO" */

/* CLASE: ValidadorDatos (extensible)
PROPOSITO: Verificar los datos manejados por la aplicación, asegurando su integridad, consistencia y validez antes de ser procesados, almacenados o enviados al back-end.
RESPONSABILIDADES:
1. Validación de Datos de Entrada: Comprueba que los datos proporcionados por el usuario o por fuentes externas cumplan con los criterios de validación específicados en los esquemas de dominio.
2. Generación de Reportes de Error: Produce reportes de los errores de validación encontrados para facilitar la corrección y la retroalimentación al usuario sobre los elementos que no cumplen las condiciones establecidas.
3. Interacción con Componentes de Datos: Trabaja en conjunto con ProcesadorEsquemas y OperadorDatos para garantizar que los datos que se procesan y almacenan sean válidos.
NOTAS: Esta clase depende de los "esquemas", donde se definen los criterios y reglas para realizar las validaciones de los datos de formularios.
Esta clase es ampliable mediante la inyección de validadores de datos, a través de la configuración dinámica que se aplica al ejecutar cada servicio.
*/
class ValidadorDatos {
    constructor() {
        this.tiposValidadoresDatos = {
            'texto': this._validarTexto,
            'entero': this._validarNumeroEntero,
            'decimal': this._validarNumeroDecimal,
            'rut': this._validarIdentificadorRUT,
            'opciones': this._validarCuantasOpcionesSeleccionadas,
            'fecha': this._validarFecha
        };
    }
    // Funciones privadas
    _validarConExpresionRegular(valor, expresion) {
        if (expresion.length > 0 && String(valor).length > 0) {
            let exp = new RegExp('^' + expresion + '$');
            return exp.test(String(valor));
        }
        return true;
    }
    _validarTexto(valor, minimo, maximo) {
        valor = String(valor).trim();
        const longitud = valor.length;
        return longitud >= minimo && (maximo === 0 || longitud <= maximo);
    }
    _validarNumeroEntero(valor, minimo, maximo) {
        const numero = parseInt(valor);
        if (isNaN(numero) || !isFinite(numero)) return false;
        return maximo > 0 ? (numero >= minimo && numero <= maximo) : (numero >= minimo);
    }
    _validarNumeroDecimal(valor, minimo, maximo) {
        const numero = parseFloat(valor);
        if (isNaN(numero) || !isFinite(numero)) return false;
        return maximo > 0 ? (numero >= minimo && numero <= maximo) : (numero >= minimo);
    }
    _validarCuantasOpcionesSeleccionadas(valor, minimo, maximo) {
        //TODO: Evaluar y corregir
        const numero = parseInt(valor);
        if (isNaN(numero) || !isFinite(numero)) return false;
        return maximo > 0 ? (numero >= minimo && numero <= maximo) : (numero >= minimo);
    }
    _validarIdentificadorRUT(valor, minimo, maximo) {
        valor = String(valor);
        if (minimo === 0 && valor.length === 0) return true;
        if (!(minimo > 0 || valor.length > 0)) return false;
        let [numero, digitoVerificador] = valor.split('-');
        if (!numero || digitoVerificador.length !== 1) return false;
        let m = 0, s = 1;
        for (; numero; numero = Math.floor(numero / 10)) {
            s = (s + numero % 10 * (9 - m++ % 6)) % 11;
        }
        const dvCalculado = s ? s - 1 : 'k';
        return String(dvCalculado).toLowerCase() === digitoVerificador.toLowerCase();
    }
    _validarFecha(valor, minimo, maximo) {
        /* Reglas que se deben cumplir:
        - Significado de "minimo": cuántos días contados desde hoy definen la fecha límite inferior aceptada.
        - Significado de "maximo": cuántos días contados desde hoy definen la fecha límite inferior aceptada.
        - Si mínimo=0 y máximo=0 implica que sólo se acepta la fecha de hoy. Pero si se cumple la condición anterior, y valor=vacío se devuelve "true", sólo se comprueba que sea la fecha de hoy si el valor no está vacío.
        Ejemplo: tomando como referencia la fecha de hoy, si la fecha ingresada debe estar en el rango de un día antes (ayer) y un día después (mañana), entonces: minimo=-1, maximo=1 */
        valor = String(valor).replace(/\//g, '-');
        if (minimo === 0 && maximo === 0) {
            return valor.length === 0 || this._esFechaDeHoy(valor);
        }
        if (valor.length === 0) return false;
        const fecha = this._parsearFecha(valor);
        if (!fecha) return false;
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        const fechaMinima = new Date(hoy);
        fechaMinima.setDate(fechaMinima.getDate() + minimo);
        const fechaMaxima = new Date(hoy);
        fechaMaxima.setDate(fechaMaxima.getDate() + maximo);
        return fecha >= fechaMinima && fecha <= fechaMaxima;
    }
    _esFechaDeHoy(valor) {
        const fecha = this._parsearFecha(valor);
        if (!fecha) return false;
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        return fecha.getTime() === hoy.getTime();
    }
    _parsearFecha(valor) {
        const partes = valor.split('-');
        if (partes.length !== 3) return null;
        const [ano, mes, dia] = partes.map(parte => parseInt(String(parte), 10));
        if (isNaN(ano) || isNaN(mes) || isNaN(dia)) return null;
        const fecha = new Date(ano, mes - 1, dia);
        fecha.setHours(0, 0, 0, 0);
        if (fecha.getFullYear() !== ano || fecha.getMonth() + 1 !== mes || fecha.getDate() !== dia) {
            return null;
        }
        return fecha;
    }
    // Funciones de configuración dinámica
    inyectarValidadoresDatos(validadores) {
        for (let identificador in validadores) {
            if (validadores.hasOwnProperty(identificador)) {
                let funcion = validadores[identificador];
                if (typeof funcion === 'function') {
                    const [tipoValidacion, nombreFuncion] = identificador.split(':');
                    this[nombreFuncion] = funcion.bind(this);
                    this.tiposValidadoresDatos[tipoValidacion] = this[nombreFuncion];
                }
            }
        }
    }
    // Funciones de verificación
    evaluarFormulario(datos, formulario) {
        Base.trazarFlujo(this.constructor.name, 'evaluarFormulario', 2);
        let estado = true;
        let errores = {};
        try {
            for (const campo in formulario.campos) {
                if (formulario.campos.hasOwnProperty(campo)) {
                    const definicion = formulario.campos[campo];
                    if (definicion) {
                        const criterios = {
                            campo: campo || '',
                            etiqueta: definicion.etiqueta || '',
                            tipo: definicion.tipo || '',
                            minimo: definicion.minimo || '',
                            maximo: definicion.maximo || '',
                            regla: definicion.regla || '',
                            error: definicion.error || '',
                            requerido: definicion.requerido || '',
                            excluir: definicion.excluir || ''
                        };
                        let valor = datos[campo] || '';
                        let resultadoValidacion = this.verificarCampo(campo, valor, criterios);
                        if (!resultadoValidacion.esValido) {
                            estado = false;
                            errores[campo] = resultadoValidacion.mensajeError;
                        }
                    }
                }
            }
        } catch (error) {
            throw error;
        }
        return { estado, errores };
    }
    verificarCampo(campo, valor, criterios) {
        Base.trazarFlujo(this.constructor.name, 'verificarCampo', 3, campo);
        try {
            let mensajeError = '';
            let esValido = true;
            if (criterios.tipo === 'novalidar') {return { esValido, mensajeError };}
            let minimo = (isNaN(parseFloat(criterios.minimo)) ? 0 : parseFloat(criterios.minimo));
            let maximo = (isNaN(parseFloat(criterios.maximo)) ? 0 : parseFloat(criterios.maximo));
            let tipo = criterios.tipo;
            esValido = this.tiposValidadoresDatos[tipo](valor, minimo, maximo) || false;
            if (esValido && criterios.regla) {
                esValido = this._validarConExpresionRegular(valor, criterios.regla);
            }
            if (!esValido) {
                mensajeError = criterios.error;
                mensajeError = mensajeError.replace('(min)', String(minimo)).replace('(max)', String(maximo)).replace('(etiqueta)', criterios.etiqueta).replace('(campo)', campo);
            }
            if (!esValido) {
                Base.trazarFlujo(this.constructor.name, 'VERIFICACION', 4, esValido, `${campo}=${valor}`, mensajeError);
            }
            return { esValido, mensajeError };
        } catch (error) {
            throw error;
        }
    }
}

/* CLASE: ComunicadorApi
PROPOSITO: Gestionar y simplificar la comunicación de la aplicación con los servicios API de back-end externos, actuando como intermediario para facilitar la realización de peticiones HTTP y el manejo de las respuestas recibidas.
RESPONSABILIDADES:
1. Realiza peticiones HTTP a servicios API, utilizando métodos como GET, POST, PUT y DELETE.
2. Procesa y adapta los datos de las peticiones y respuestas para asegurar la compatibilidad con los formatos esperados por la aplicación y los servicios API.
3. Maneja la autenticación y autorización, incluyendo el manejo de tokens de acceso y claves de API.
4. Proporciona una interfaz unificada para realizar peticiones a diferentes servicios API, abstrayendo detalles específicos de cada API.
5. Gestiona errores de comunicación y respuestas inesperadas de las API, implementando mecanismos de recuperación y notificación de errores.
NOTAS:
Esta clase depende de los adaptadores de API específicos (subclases de "AdaptadorApi") para manejar las particularidades de cada servicio API con el que se comunica.
*/
class ComunicadorApi {
    constructor(gestorEstado) {
        this.gestorEstado = gestorEstado;
        this.adaptadorApi = null;
    }
    // Funciones privadas
    _configurarPeticionApi(metodo, datos) {
        let { encabezados, cuerpo } = this.adaptadorApi.construirPeticion(datos);
        if (metodo === 'GET') {
            cuerpo = null;
        }
        Base.trazarFlujo('ComunicadorApi', '_configurarPeticionApi:CUERPO', 4, cuerpo);
        return {
            method: metodo,
            headers: encabezados,
            body: datos ? cuerpo : null
        };
    }
    async _recibirRespuestaApi(respuesta) {
        try {
            if (respuesta.ok) {
                return await respuesta.json();
            } else {
                throw new ErrorPersonalizado('ERROR_RESPUESTA_API', respuesta.statusText, {}, respuesta.status);
            }
        } catch (error) {
            throw new ErrorPersonalizado('ERROR_FORMATO_DE_RESPUESTA', error.message);
        }
    }
    _manejarErroresComunicacion(error) {
        if (error.name === 'AbortError') {
            throw new ErrorPersonalizado('ERROR_PETICION_TIEMPO_SUPERADO', error.message, {}, 408);
        }
        if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
            throw new ErrorPersonalizado('ERROR_SERVICIO_NO_DISPONIBLE', error.message, {}, 503);
        }
        if (error instanceof ErrorPersonalizado) {
            throw error;
        }
        throw new ErrorPersonalizado('ERROR_PETICION_NO_REALIZADA', error.message);
    }
    // Funciones para datos de la aplicación
    async consultarManifiestoApp(rutaManifiesto) {
        Base.trazarFlujo(this.constructor.name, 'consultarManifiestoApp', 2, rutaManifiesto);
        try {
            if (rutaManifiesto) {
                const urlManifiesto = Base.construirUrlAbsoluta(rutaManifiesto);
                const respuesta = await fetch(urlManifiesto, {cache: "no-cache"});
                if (!respuesta.ok) {
                    throw new ErrorPersonalizado('ERROR_CARGAR_MANIFIESTO', respuesta.statusText, {"url": urlManifiesto}, respuesta.status);
                }
                const manifiesto = await respuesta.json();
                const { name, short_name, description, start_url, scope } = manifiesto;
                const datosManifiesto = {"nombre": name, "nombre_corto": short_name, "descripcion": description, "alcance": scope, "url_inicio": start_url};
                this.gestorEstado.actualizarEstado('', Base.Estados.aplicacion, datosManifiesto);
                document.title = short_name;
            }
        } catch (error) {
            throw error;
        }
    }
    async enviarPeticionJson(urlReceptor, datos, metodo='POST') {
        Base.trazarFlujo(this.constructor.name, 'enviarPeticionJson', 2, `${metodo}: ${urlReceptor}`);
        try {
            const datosJSON = JSON.stringify(datos);
            Base.trazarFlujo(this.constructor.name, 'enviarPeticionJson:PETICION', 4, datosJSON);
            const respuesta = await fetch(urlReceptor, {
                method: metodo,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Accept': 'application/json'
                },
                body: datosJSON,
            });
            const resultado = await respuesta.json();
            if (!respuesta.ok) {
                let mensaje = respuesta.statusText;
                if (resultado.mensaje) {
                    mensaje = resultado.mensaje;
                }
                throw new ErrorPersonalizado('ERROR_ENVIAR_DATOS', mensaje, {"url": urlReceptor}, respuesta.status);
            }
            Base.trazarFlujo(this.constructor.name, 'enviarPeticionJson:RESULTADO', 4, resultado);
            return resultado;
        } catch (error) {
            throw error;
        }
    }
    // Funciones para comunicación con API
    async configurarApi(uidApi, urlApi, keyApi) {
        Base.trazarFlujo(this.constructor.name, 'configurarApi', 2, `uidApi=${uidApi}`, `urlApi=${urlApi}`);
        try {
            this.adaptadorApi = await CreadorAdaptadoresApi.crearAdaptador(this.gestorEstado, uidApi);
            if (this.adaptadorApi) {
                this.adaptadorApi.urlApi = urlApi;
                this.adaptadorApi.keyApi = keyApi;
                this.adaptadorApi.gestorEstado = this.gestorEstado;
                this.adaptadorApi.uuid = this.gestorEstado.obtenerValor(Base.Estados.sesion, 'uuid');
                this.adaptadorApi.token = this.gestorEstado.obtenerValor(Base.Estados.sesion, 'token');
            }
        } catch (error) {
            throw error;
        }
    }
    async realizarPeticionApi(puntofinal, metodo, datos={}, parametros={}, limiteTiempo=10) {
        Base.trazarFlujo(this.constructor.name, 'realizarPeticionApi', 2, metodo, puntofinal, limiteTiempo);
        const controlador = new AbortController();
        const temporizador = setTimeout(() => controlador.abort(), (limiteTiempo * 1000));
        try {
            this.adaptadorApi.validarMetodoEnvio(metodo);
            const url = this.adaptadorApi.crearUrlCompleta(puntofinal, parametros);
            const opciones = this._configurarPeticionApi(metodo, datos);
            const signal = { signal: controlador.signal };
            const respuesta = await fetch(url, { ...opciones, ...signal });
            clearTimeout(temporizador);
            return await this._recibirRespuestaApi(respuesta);
        } catch (error) {
            clearTimeout(temporizador);
            return this._manejarErroresComunicacion(error);
        }
    }
    adaptarRespuestaApi(respuesta) {
        Base.trazarFlujo(this.constructor.name, 'RESPUESTA', 4, respuesta);
        Base.trazarFlujo(this.constructor.name, 'adaptarRespuestaApi', 2);
        try {
            if (!respuesta || typeof respuesta !== 'object') {
                throw new ErrorPersonalizado('ERROR_RESPUESTA_NO_PROCESADA');
            }
            return this.adaptadorApi.adaptarRespuesta(respuesta);
        } catch (error) {
            throw error;
        }
    }
}

/* CLASE: CreadorAdaptadoresApi (estática)
PROPOSITO: Crear y gestionar de instancias de adaptadores de API específicos. Su función principal es proporcionar una forma centralizada de obtener adaptadores de API personalizados para interactuar con diversos servicios de back-end.
RESPONSABILIDADES:
1. Crea y configura instancias de adaptadores de API basados en las especificaciones de la aplicación y las necesidades de cada servicio API.
2. Garantiza que se utilice el adaptador de API correcto para cada servicio, en función de su URL, tipo y otros parámetros de configuración.
3. Provee un punto de acceso único para la obtención de adaptadores de API, mejorando la organización y reutilización del código.
4. Asegura la correcta inicialización de los adaptadores de API, incluyendo la asignación de claves de API, tokens de acceso y otros parámetros necesarios para la comunicación.
NOTAS:
Depende de la clase "AdaptadorApi" y sus subclases, las cuales definen la estructura y comportamiento de los adaptadores de API específicos.
*/
class CreadorAdaptadoresApi {
    static async crearAdaptador(gestorEstado, uidApi) {
        Base.trazarFlujo('CreadorAdaptadoresApi', 'crearAdaptador', 3, `uidApi=${uidApi}`);
        let adaptador = null;
        try {
            const estadosModelo = gestorEstado.obtenerEstado(Base.Estados.modelo);
            const serviciosApi = estadosModelo.get('serviciosApi');
            if (serviciosApi && serviciosApi[uidApi]) {
                const { rutaAdaptador } = serviciosApi[uidApi];
                const urlAdaptador = Base.construirUrlAbsoluta(rutaAdaptador);
                const moduloAdaptador = await import(urlAdaptador);
                if (moduloAdaptador) {
                    adaptador = moduloAdaptador.adaptador;
                }
            }
        } catch (error) {
            throw error;
        }
        return adaptador;
    }
}


/* **************************************************************************** */
/* CLASES COMPLEMENTARIAS DEL AMBITO DEL "PRESENTADOR" */

/* CLASE: ControladorAcceso
PROPOSITO: Administrar y aplicar las políticas de seguridad para el control de acceso dentro de la aplicación, garantizando que las interacciones, operaciones y datos sean accedidos únicamente por usuarios autorizados que cumplan los requisitos establecidos en los esquemas de la aplicación.
RESPONSABILIDADES:
1. Gestión de Autenticación y Roles: Administra el proceso de autenticación de usuarios, incluyendo el inicio y cierre de sus sesiones.
2. Seguridad de Sesión: Mantiene la integridad y seguridad de las sesiones de usuario, gestionando aspectos como tokens de autenticación y tiempos de expiración.
3. Control de Acceso Basado en Roles: Verifica las autorizaciones de los usuarios a los diferentes servicios y componentes de la aplicación, en función de sus roles asignados como credenciales y de los permisos de acceso definidos en los esquemas.
NOTAS:
A través de esta clase, en combinación con el uso de esquemas de dominio y de interacciones, se implementa un robusto sistema de control de acceso basado en roles (RBAC), esencial para aplicaciones multiusuario y para garantizar la seguridad y el acceso apropiado a las funcionalidades en las aplicaciones de mayor complejidad.
*/
class ControladorAcceso {
    constructor(gestorEstado) {
        this.gestorEstado = gestorEstado;
    }
    // Funciones privadas para validaciones
    _validarCadenaNoVacia(valor, nombre) {
        if (typeof valor !== 'string' || valor.trim() === '') {
            throw new ErrorPersonalizado('ERROR_PARAMETRO_VACIO', '', {"nombre": nombre});
        }
    }
    _manejarTokenAutenticacion(token, duracionEnHoras=null) {
        const path = window.location.pathname;
        try {
            if (duracionEnHoras) {
                const fechaExpiracion = new Date();
                fechaExpiracion.setTime(fechaExpiracion.getTime() + (duracionEnHoras * 60 * 60 * 1000));
                const expires = "expires=" + fechaExpiracion.toUTCString();
                document.cookie = "token=" + token + ";" + expires + ";path=" + path;
            } else {
                document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=" + path;
            }
            return path;
        } catch (error) {
            throw error;
        }
    }
    _recuperarDatosAutenticados(datos) {
        try {
            const { token, idusuario, alias, email, roles, imagen, inicio, idioma, duracionEnHoras=10 } = datos;
            const alcance = this._manejarTokenAutenticacion(token, duracionEnHoras);
            if (token && idusuario && roles) {
                const datosSesion = {
                    token: token,
                    alcance: alcance,
                    idusuario: idusuario,
                    alias: alias,
                    email: email,
                    imagen: imagen,
                    inicio: inicio,
                    idioma: idioma,
                    roles: roles
                }
                return datosSesion;
            }
        } catch (error) {
            throw error;
        }
        return null;
    }
    // Funciones para autorización según roles
    autorizarPorRoles(permisosAcceso, rolesCredenciales) {
        Base.trazarFlujo(this.constructor.name, 'autorizarPorRoles', 3, `permisosAcceso=${permisosAcceso}`, `rolesCredenciales=${rolesCredenciales}`);
        try {
            if (typeof permisosAcceso === 'undefined') { return true; }
            if ((permisosAcceso === '*' && rolesCredenciales)) { return true; }
            if (!rolesCredenciales || !permisosAcceso) { return null; }
            const rolesUsuario = rolesCredenciales.split(',');
            const rolesInteraccion = permisosAcceso.split(',');
            return rolesInteraccion.some(rolInteraccion => rolesUsuario.includes(rolInteraccion.trim()));
        } catch (error) {
            throw error;
        }
    }
    filtrarPorRoles(listaElementos, rolesCredenciales) {
        Base.trazarFlujo('ControladorAcceso', 'filtrarPorRoles', 4, `rolesCredenciales=${rolesCredenciales}`);
        try {
            if (!listaElementos) return {};
            if (!rolesCredenciales) { rolesCredenciales = ''; }
            const rolesEvaluar = rolesCredenciales.split(',');
            let elementosFiltrados = {};
            Object.keys(listaElementos).forEach(clave => {
                const elemento = listaElementos[clave];
                if (typeof elemento.permisos === 'undefined' || (elemento.permisos === '*' && rolesCredenciales)) {
                    elementosFiltrados[clave] = elemento;
                } else {
                    const rolesElemento = elemento.permisos.split(',');
                    if (rolesElemento.some(rolElemento => rolesEvaluar.includes(rolElemento.trim()))) {
                        elementosFiltrados[clave] = elemento;
                    };
                }
            });
            return elementosFiltrados;
        } catch (error) {
            throw error;
        }
    }
    // Funciones para manejo de sesiones
    registrarDatosSesion(datos) {
        Base.trazarFlujo(this.constructor.name, 'registrarDatosSesion', 3);
        if (datos && datos.sesion) {
            const datosSesion = this._recuperarDatosAutenticados(datos.sesion);
            this.gestorEstado.actualizarEstado('', Base.Estados.sesion, datosSesion, true);
            return true;
        }
        return false;
    }
    vaciarDatosSesion() {
        Base.trazarFlujo(this.constructor.name, 'vaciarDatosSesion', 3);
        try {
            this.gestorEstado.actualizarEstado('', Base.Estados.sesion, null, true);
            return this.borrarTokenAutenticacion();
        } catch (error) {
            throw error;
        }
    }
    // Funciones para manejo de autenticación
    obtenerTokenAutenticacion() {
        Base.trazarFlujo(this.constructor.name, 'obtenerTokenAutenticacion', 3);
        let token = '';
        try {
            let valor = `; ${document.cookie}`;
            let partes = valor.split('; token=');
            if (partes.length === 2) {
                token = partes.pop().split(';').shift();
            }
        } catch (error) {
            throw error;
        }
        return token;
    }
    borrarTokenAutenticacion() {
        Base.trazarFlujo(this.constructor.name, 'borrarTokenAutenticacion', 3);
        try {
            return this._manejarTokenAutenticacion('', null);
        } catch (error) {
            throw error;
        }
    }
}

/* CLASE: ProcesadorEsquemas
PROPOSITO: Manejar y proporcionar acceso a los "esquemas de dominio" de los servicios que se utilizan en las distintas capas de la aplicación. Estos esquemas definen estructural y funcionalmente la arquitectura y el comportamiento del Modelo de cada uno de los servicios de la aplicación.
RESPONSABILIDADES:
1. Carga y Actualización de Esquemas: Obtiene dinámicamente los esquemas correspondientes a cada interacción, además de procesar dichos esquemas para validarlos y aplicar en ellos las políticas de control de acceso para que garanticen su consistencia, adecuación y seguridad.
2. Especificaciones para la Vista: Entrega esquemas que suministran "moldes para dibujar" en la Vista los componentes de datos (de entrada y salida) y de interacción, utilizando plantillas para mostrar, imprimir y exportar los datos, y adaptando dinámicamente su visualización en la interfaz de usuario según las autorizaciones de acceso.
3. Validación y Empaquetamiento de Datos: Entrega esquemas que proporcionan "reglas de verificación" para validar y estructurar los datos que se envían al back-end en las diferentes operaciones de administración de datos, asegurando que cumplan con las especificaciones requeridas y las políticas de seguridad.
4. Soporte a la Lógica del Presentador: Entrega esquemas que proveen "definiciones de interaccionea" para organizar la lógica de la aplicación, incluyendo el control de acceso basado en roles para segmentar todos los aspectos relevantes.
5. Soporte a la Navegación: Entrega esquemas que contribuyen a generar "mapas de navegación funcional y contextual" dentro de la aplicación, apoyando la interconexión coherente, cohesionada y organizada entre diferentes recursos y servicios.
NOTAS:
1. Definición de esquemas: Los esquemas son estructuras de datos representadas en formato JSON que se utilizan para declarar y describir detalladamente los distintos componentes lógicos del dominio. Esto incluye aspectos como la composición, atributos, reglas y permisos de acceso para formularios (entradas), informes y listados (salidas), diccionarios de datos (metadatos), rutas de navegación (funcional y contextual), autómatas de estados, flujos de trabajo, etc., así como de todas las interacciones involucradas en ellos. Se usan en forma transversal en las diferentes capas de la aplicación.
2. Aplicaciones de los esquemas en diferentes capas y ámbitos:
- Diseño de Formularios en UI: Establecen cómo se deben organizar, presentar y configurar los formularios y elementos de UI asociados, incluyendo campos, grupos, leyendas, etiquetas, textos de ayuda, botones de interacción, y opciones para visualizar los campos y grupos.
- Diseño de Informes en UI: Establecen cómo se deben organizar, presentar y manejar los informes y listados de datos, junto con sus herramientas de recuperación, incluyendo filtros, columnas, formatos, etiquetas, leyendas, botones de interacción y opciones para visualizar y diagramar columnas y filas.
- Políticas de Acceso por Roles: Establecen reglas y permisos basados en roles para determinar el acceso a todos los componentes lógicos del Modelo y sus elementos, ofreciendo un alto grado de flexibilidad y granularidad para configurar múltiples escenarios y casos de uso.
- Diccionarios de Datos y Metadatos: Proveen un conjunto organizado de valores y atributos que se usan en distintas partes de la aplicación, para garantizar la accesibilidad y consistencia de los vocabularios controlados que se aplican en los descriptores y catalogadores de información.
- Criterios de Comprobación de Datos: Establecen reglas para realizar las comprobaciones de tipos y las validaciones del nombre y contenido de los datos de formularios, asegurando que cumplan con los criterios y condiciones específicas establecidas para todos ellos.
- Rutas Funcionales y Contextuales: Proveen un conjunto seleccionado de rutas virtuales para acceder a las interacciones disponibles y autorizadas en cada servicio, junto con los parámetros y opciones que constituyen su contexto de ejecución (servicio, recurso, operacion, esquema, plantilla, uid, etc.).
Los esquemas han sido diseñados dentro de la arquitectura con una orientación hacia el dominio, adoptando principios de Domain-Driven Design (DDD). Esto facilita una comprensión más profunda y una modelización precisa de los problemas y sus soluciones, permitiendo así un mayor alineamiento entre los requerimientos del negocio y la aplicación implementada. Este enfoque fomenta la colaboración entre desarrolladores y expertos del dominio, promoviendo un lenguaje ubicuo que mejora la comunicación y la claridad del diseño de la aplicación. Al incorporar DDD en su arquitectura, la biblioteca no solo mejora la mantenibilidad y escalabilidad de las aplicaciones desarrolladas con ella, sino que también ofrece una base sólida para el crecimiento y la evolución futura del software, siguiendo los principios del diseño y arquitectura limpios.
*/
class ProcesadorEsquemas {
    constructor() {
        this.rutaEsquemas = '';
        this.rolesUsuario = '';
    }
    // Funciones privadas
    _filtrarFormulario(formulario, funcionFiltro) {
        try {
            if (formulario && typeof formulario === 'object' && typeof funcionFiltro === 'function') {
                formulario.grupos = funcionFiltro(formulario.grupos, this.rolesUsuario);
                formulario.campos = funcionFiltro(formulario.campos, this.rolesUsuario);
                formulario.interacciones = funcionFiltro(formulario.interacciones, this.rolesUsuario);
            }
        } catch (error) {
            throw error;
        }
        return formulario;
    }
    _filtrarInforme(informe, funcionFiltro) {
        try {
            if (informe && typeof informe === 'object' && typeof funcionFiltro === 'function') {
                informe.opciones = funcionFiltro(informe.opciones, this.rolesUsuario);
                informe.parametros = funcionFiltro(informe.parametros, this.rolesUsuario);
                informe.resultados = funcionFiltro(informe.resultados, this.rolesUsuario);
                informe.interacciones = funcionFiltro(informe.interacciones, this.rolesUsuario);
                informe.enlaces = funcionFiltro(informe.enlaces, this.rolesUsuario);
            }
        } catch (error) {
            throw error;
        }
        return informe;
    }
    _filtrarDiccionario(diccionario, funcionFiltro) {
        try {
            if (diccionario && typeof diccionario === 'object' && typeof funcionFiltro === 'function') {
                const diccionarioFiltrado = {};
                Object.keys(diccionario).forEach(concepto => {
                    let objetoValores = diccionario[concepto];
                    let valores = [];
                    Object.entries(objetoValores).forEach(([clave, valor]) => {
                        valores.push(valor);
                    });
                    diccionarioFiltrado[concepto] = funcionFiltro(valores, this.rolesUsuario);
                });
                diccionario = {};
                Object.keys(diccionarioFiltrado).forEach(clave => {
                    diccionario[clave] = Object.values(diccionarioFiltrado[clave]);
                });
            }
        } catch (error) {
            throw error;
        }
        return diccionario;
    }
    _filtrarNavegacion(navegacion, funcionFiltro) {
        try {
            if (navegacion && typeof navegacion === 'object' && typeof funcionFiltro === 'function') {
                navegacion = funcionFiltro(navegacion, this.rolesUsuario);
            }
        } catch (error) {
            throw error;
        }
        return navegacion;
    }
    _fusionarEsquemas(completo, reducido) {
        try {
            Object.keys(reducido).forEach(clave => {
                const valorCompleto = completo[clave];
                const valorReducido = reducido[clave];
                if (typeof valorCompleto === 'object' && valorCompleto && typeof valorReducido === 'object' && valorReducido) {
                    completo[clave] = this._fusionarEsquemas(Object.assign({}, valorCompleto), valorReducido);
                } else {
                    completo[clave] = valorReducido;
                }
            });
        } catch (error) {
            throw error;
        }
        return completo;
    }
    async _cargarEsquemas(seleccion, idioma='') {
        try {
            let rutaEsquemas = this.rutaEsquemas;
            if (idioma) {
                rutaEsquemas = rutaEsquemas.replace('.json', `-${idioma}.json`);
            }
            const respuesta = await fetch(rutaEsquemas);
            if (!respuesta.ok) { return null; }
            const esquemas = await respuesta.json();
            if (!esquemas) {
                throw new ErrorPersonalizado('ERROR_ESQUEMAS_NO_CARGADOS', '', {"ruta": rutaEsquemas});
            }
            return {
                formulario: seleccion.formulario ? esquemas.formularios.find(f => f.id === seleccion.formulario) : null,
                informe: seleccion.informe ? esquemas.informes.find(i => i.id === seleccion.informe) : null,
                diccionario: seleccion.diccionario ? esquemas.diccionarios[seleccion.diccionario] : null,
                navegacion: seleccion.navegacion ? esquemas.navegacion[seleccion.navegacion] : null
            }
        } catch (error) {
            throw error;
        }
    }
    // Funciones públicas
    asignarParametros(rolesUsuario=null, rutaEsquemas=null) {
        Base.trazarFlujo(this.constructor.name, 'asignarParametros', 3, `rolesUsuario=${rolesUsuario}`, `rutaEsquemas=${rutaEsquemas}`);
        if (rutaEsquemas) {
            this.rutaEsquemas = rutaEsquemas;
        }
        if (rolesUsuario) {
            this.rolesUsuario = rolesUsuario;
        }
    }
    async importarEsquemas(portadorInformacion) {
        Base.trazarFlujo(this.constructor.name, 'importarEsquemas', 3);
        try {
            if ( !portadorInformacion.FORMULARIO && !portadorInformacion.INFORME && 
                (portadorInformacion.peticion.formulario || portadorInformacion.peticion.informe || portadorInformacion.peticion.servicio) ) {
                const servicio = portadorInformacion.peticion.servicio || '';
                const seleccion = {
                    "formulario": portadorInformacion.peticion.formulario, 
                    "informe": portadorInformacion.peticion.informe, 
                    "diccionario": servicio, 
                    "navegacion": servicio
                };
                const idiomaElegido = portadorInformacion.gestorEstado.obtenerValor(Base.Estados.preferencias, 'idioma');
                const esquemasCompletos = await this._cargarEsquemas(seleccion);
                const esquemasReducidos = await this._cargarEsquemas(seleccion, idiomaElegido);
                let esquemasFusionados = esquemasCompletos;
                if (esquemasReducidos) {
                    esquemasFusionados = this._fusionarEsquemas(esquemasCompletos, esquemasReducidos);
                }
                portadorInformacion.guardarEsquemas(esquemasFusionados);
            }
        } catch (error) {
            throw error;
        }
    }
    filtrarEsquemas(portadorInformacion, funcionFiltro) {
        Base.trazarFlujo(this.constructor.name, 'filtrarEsquemas', 3);
        try {
            if (portadorInformacion.FORMULARIO) {
                portadorInformacion.FORMULARIO = this._filtrarFormulario(portadorInformacion.FORMULARIO, funcionFiltro);
            }
            if (portadorInformacion.INFORME) {
                portadorInformacion.INFORME = this._filtrarInforme(portadorInformacion.INFORME, funcionFiltro);
            }
            if (portadorInformacion.DICCIONARIO) {
                portadorInformacion.DICCIONARIO = this._filtrarDiccionario(portadorInformacion.DICCIONARIO, funcionFiltro);
            }
            if (portadorInformacion.NAVEGACION) {
                portadorInformacion.NAVEGACION = this._filtrarNavegacion(portadorInformacion.NAVEGACION, funcionFiltro);
            }
        } catch (error) {
            throw error;
        }
    }
    transformarEsquemas(portadorInformacion) {
        //TODO: Pendiente
    }
}

/* CLASE: PortadorInformacion
PROPOSITO: Manejar y transportar el estado específico de cada interacción en la aplicación durante su ciclo de vida. Actúa como un "Data Transfer Object" (DTO) "enriquecido", que facilita el traspaso de información del contexto entre las diferentes capas de la aplicación en un entorno asincrónico y dinámico.
RESPONSABILIDADES:
1. Manejo del Estado de Interacción: Gestiona el estado asociado a cada acción individual o interacción dentro de la aplicación, desde el inicio hasta el final de su ciclo de vida (petición-respuesta, acción-reacción).
2. Transporte de Información: Facilita la transferencia de datos, metadatos y esquemas entre componentes, servicios y capas de la aplicación, manteniendo la coherencia y relevancia de la información en cada etapa.
3. Soporte a Operaciones Asincrónicas: Proporciona un mecanismo efectivo para manejar operaciones asincrónicas, acoplándose al sistema de publicación/suscripción de eventos de cambio, asegurando que el estado y los datos asociados a cada proceso se mantengan íntegros y accesibles a lo largo de su ejecución.
NOTAS:
Es administrado por el CoordinadorGeneral y utilizada especialmente es componentes y funciones que implementan interacciones asincrónicas y dinámicas.
Es esencial para mantener la coherencia del flujo de datos en operaciones complejas y para la gestión eficiente de estados temporales.
Juega un rol clave en el traspaso y sincronización de información entre la Interfaz de Usuario (Vista) y el Administrador de Datos (Modelo), potenciando la comunicación y colaboración entre estas capas.
*/
class PortadorInformacion {
    constructor(gestorEstado=null) {
        this.gestorEstado = gestorEstado;
        this.FORMULARIO = null;
        this.INFORME = null;
        this.DICCIONARIO = null;
        this.NAVEGACION = null;
        this.peticion = {};
        this.caso = {};
        this.lista = {};
        this.respuesta = {"codigo": "", "tipo": "", "mensaje": ""};
        this.errores = null;
        this.servicio = '';
    }
    // Funciones privadas
    _validarDatos(datos) {
        return datos && typeof datos === 'object' && (datos.caso || datos.lista || datos.resultado || datos.mensaje || datos.codigo);
    }
    _validarEsquemas(esquemas) {
        return esquemas && typeof esquemas === 'object' && (esquemas.informe || esquemas.formulario || esquemas.diccionario || esquemas.navegacion);
    }
    // Funciones de escritura / actualización
    asignarErrores(errores) {
        Base.trazarFlujo(this.constructor.name, 'asignarErrores', 3);
        try {
            this.errores = null;
            if (errores) {
                this.errores = errores;
            }
        } catch (error) {
            throw error;
        }
    }
    prepararPeticion(operacion, contexto) {
        Base.trazarFlujo(this.constructor.name, 'prepararPeticion', 3, `operacion=${operacion}`);
        try {
            this.peticion['operacion'] = operacion || '';
            const { recurso, uid, valores, parametros, formulario, informe, validar, selector, plantilla, servicio } = contexto;
            this.servicio = servicio || '';
            this.peticion['servicio'] = this.servicio;
            this.peticion['uid'] = uid || '';
            this.peticion['recurso'] = recurso || '';
            this.peticion['formulario'] = formulario || '';
            this.peticion['informe'] = informe || '';
            this.peticion['valores'] = valores || {};
            this.peticion['parametros'] = parametros || {};
            this.peticion['selector'] = selector || '';
            this.peticion['plantilla'] = plantilla || '';
        } catch (error) {
            throw error;
        }
    }
    almacenarInformacion(datos, vaciar=true) {
        Base.trazarFlujo(this.constructor.name, 'almacenarInformacion', 3, `vaciar=${vaciar}`);
        try {
            if (!this._validarDatos(datos)) {
                throw new ErrorPersonalizado('ERROR_FORMATO_DE_DATOS');
            }
            if (vaciar) {
                this.caso = {};
                this.lista = {};
                this.respuesta = {"codigo": "", "tipo": "", "mensaje": ""};
            }
            const { resultado=null, caso=null, lista=null, esquemas=null, codigo, tipo, mensaje } = datos;
            this.caso = resultado?.caso || caso;
            this.lista = resultado?.lista || lista;
            this.respuesta = {
                codigo: codigo || '',
                tipo: tipo || '',
                mensaje: mensaje || ''
            };
            if (esquemas) {
                this.guardarEsquemas(esquemas);
            }
            return this.recuperarInformacion('datos');
        } catch (error) {
            throw error;
        }
    }
    guardarEsquemas(esquemas, vaciar=true) {
        Base.trazarFlujo(this.constructor.name, 'guardarEsquemas', 3, `vaciar=${vaciar}`);
        try {
            if (!esquemas) { return; }
            if (!this._validarEsquemas(esquemas)) {
                throw new ErrorPersonalizado('ERROR_FORMATO_DE_ESQUEMAS');
            }
            if (vaciar) {
                this.FORMULARIO = null;
                this.INFORME = null;
                this.DICCIONARIO = null;
                this.NAVEGACION = null;
            }
            this.FORMULARIO = esquemas.formulario || this.FORMULARIO;
            this.INFORME = esquemas.informe || this.INFORME;
            this.DICCIONARIO = esquemas.diccionario || this.DICCIONARIO;
            this.NAVEGACION = esquemas.navegacion || this.NAVEGACION;
        } catch (error) {
            throw error;
        }
    }
    // Funciones de lectura / recuperación
    recuperarInformacion(tipo='todo') {
        Base.trazarFlujo(this.constructor.name, 'recuperarInformacion', 3, `tipo=${tipo}`);
        try {
            const mapeoInformacion = {
                'datos': () => ({
                    respuesta: this.respuesta,
                    caso: this.caso,
                    lista: this.lista
                }),
                'esquemas': () => ({
                    formulario: this.FORMULARIO,
                    informe: this.INFORME,
                    diccionario: this.DICCIONARIO,
                    navegacion: this.NAVEGACION
                }),
                'errores': () => this.errores,
                'peticion': () => this.peticion,
                'respuesta': () => this.respuesta
            };
            if (tipo && tipo !== 'todo') {
                return mapeoInformacion[tipo] ? mapeoInformacion[tipo]() : null;
            } else {
                return {
                    codigo: this.respuesta['codigo'] || '',
                    mensaje: this.respuesta['mensaje'] || '',
                    tipo: this.respuesta['tipo'] || '',
                    servicio: this.servicio,
                    peticion: this.peticion,
                    errores: this.errores,
                    esquemas: {
                        formulario: this.FORMULARIO,
                        informe: this.INFORME,
                        diccionario: this.DICCIONARIO,
                        navegacion: this.NAVEGACION
                    },
                    datos: {
                        caso: this.caso,
                        lista: this.lista,
                        respuesta: this.respuesta,
                        sesion: Object.fromEntries(this.gestorEstado.obtenerEstado(Base.Estados.sesion)),
                        aplicacion: Object.fromEntries(this.gestorEstado.obtenerEstado(Base.Estados.aplicacion))
                    },
                    plantilla: this.peticion['plantilla'] || '',
                    informe: this.peticion['informe'] || ''
                };
            }
        } catch (error) {
            throw error;
        }
    }
}

/* CLASE: ManejadorErrores
PROPOSITO: Manejar y procesar los errores generados en la aplicación, transformándolos en un formato estandarizado y registrándolos para su seguimiento y análisis.
RESPONSABILIDADES:
1. Procesamiento de Errores: Clasificar y procesar diferentes tipos de errores (personalizados y estándar) y convertirlos en un formato uniforme para su manejo.
2. Registro de Errores: Utilizar una instancia de RegistradorErrores para registrar los detalles de los errores procesados.
3. Normalización de Errores: Proveer una interfaz común para el manejo de errores, independientemente de su origen o tipo.
NOTAS:
Esta clase forma parte del sistema de gestión de errores de la biblioteca, e interactúa con RegistradorErrores y ErrorPersonalizado.
*/
class ManejadorErrores {
    constructor(traductorIdiomas, urlRespaldo) {
        this.registradorErrores = new RegistradorErrores(urlRespaldo, 50);
        this.traductorIdiomas = traductorIdiomas;
    }
    // Funciones privadas
    _procesarErrorEstandar(error) {
        return {
            'codigo': 2, 
            'tipo': Base.Mensajes.ERROR,
            'mensaje': `${this.traductorIdiomas._('ERROR_ESTANDAR')}: ${error.message}`
        };
    }
    _procesarErrorDesconocido() {
        return {
            'codigo': 1, 
            'tipo': Base.Mensajes.ERROR,
            'mensaje': this.traductorIdiomas._('ERROR_DESCONOCIDO')
        };
    }
    _procesarErrorPersonalizado(error) {
        let mensaje = error.message;
        if (error.plantilla.length >0 && this.traductorIdiomas.TEXTOS.has(error.plantilla)) {
            const respuesta = {"respuesta": mensaje};
            const contexto = {...error.contexto, ...respuesta };
            mensaje = Base.reemplazarMarcadores(this.traductorIdiomas._(error.plantilla), contexto);
        }
        return {
            'mensaje': mensaje,
            'codigo': error.codigo, 
            'tipo': error.tipo,
            'contexto': error.contexto
        };
    }
    // Funciones públicas
    procesarError(error, detalles={}) {
        Base.trazarFlujo(this.constructor.name, 'procesarError', 3);
        console.error(error, detalles);
        let errorProcesado;
        if (error instanceof ErrorPersonalizado) {
            errorProcesado = this._procesarErrorPersonalizado(error);
        } else if (error instanceof Error) {
            errorProcesado = this._procesarErrorEstandar(error);
        } else {
            errorProcesado = this._procesarErrorDesconocido();
        }
        if (this.registradorErrores) {
            this.registradorErrores.registrarError(errorProcesado, detalles);
        }
        return errorProcesado;
    }
}

/* CLASE: RegistradorErrores
PROPOSITO: Registrar y almacenar errores generados en la aplicación para su análisis y seguimiento, y respaldarlos en un servidor externo.
RESPONSABILIDADES:
1. Registro de Errores: Almacenar los errores procesados por ManejadorErrores.
2. Respaldo de Errores: Enviar los registros de errores a un servidor para su conservación y análisis.
3. Gestión de Registros: Mantener un límite en la cantidad de registros almacenados y limpiar los registros una vez respaldados.
NOTAS:
Esta clase forma parte del sistema de gestión de errores de la biblioteca e interactúa con ManejadorErrores.
*/
class RegistradorErrores {
    constructor(urlRespaldo, limiteRegistros=50) {
        this.REGISTROS = [];
        this.limiteRegistros = limiteRegistros;
        this.urlRespaldo = urlRespaldo;
    }
    // Funciones privadas
    _detectarTipoDispositivo() {
        const esMobil = /Mobi|Android/i.test(navigator.userAgent);
        return esMobil ? 'Móvil' : 'Escritorio';
    }
    // Funciones públicas
    registrarError(error, detalles, niveles=['danger']) {
        Base.trazarFlujo(this.constructor.name, 'registrarError', 3);
        try {
            if (!niveles.includes(String(error.tipo))) { return; }
            const infoAdicional = {
                navegador: navigator.userAgent,
                resolucionPantalla: `${window.innerWidth}x${window.innerHeight}`,
                tipoDispositivo: this._detectarTipoDispositivo()
            };
            const fechaHora = new Date().toISOString();
            const mensajeError = `Tipo: ${error.tipo}, Fecha: ${fechaHora}, Error: ${error.mensaje}, Contexto: ${JSON.stringify(detalles)}, Info: ${JSON.stringify(infoAdicional)}`;
            this.REGISTROS.push(mensajeError);
            if (this.REGISTROS.length > this.limiteRegistros) {
                //this.REGISTROS.shift();
                this.respaldarRegistros();
            }
        } catch (error) {
            console.error(error);
        }
    }
    async respaldarRegistros(reintentosMaximos=3, esperaInicial=1000) {
        Base.trazarFlujo(this.constructor.name, 'respaldarRegistros', 3, `url=${this.urlRespaldo}`);
        let intentos = 0;
        let espera = esperaInicial;
        const intentarRespaldo = async () => {
            try {
                if (!this.urlRespaldo) {
                    throw new ErrorPersonalizado('ERROR_URL_NO_VALIDA');
                }
                const respuesta = await fetch(this.urlRespaldo, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(this.REGISTROS)
                });
                if (!respuesta.ok) {
                    throw new ErrorPersonalizado('ERROR_RESPALDAR_REGISTROS', respuesta.statusText, {"ruta": this.urlRespaldo}, respuesta.status);
                }
                this.vaciarRegistros();
            } catch (error) {
                if (intentos < reintentosMaximos) {
                    setTimeout(intentarRespaldo, espera);
                    espera *= 2;
                    intentos++;
                } else {
                    throw error;
                }
            }
        };
        await intentarRespaldo();
    }
    vaciarRegistros() {
        Base.trazarFlujo(this.constructor.name, 'vaciarRegistros', 3);
        this.REGISTROS = [];
    }
}

/* CLASE: ErrorPersonalizado (subclase)
PROPOSITO: Extender la clase Error estándar de JavaScript para proporcionar errores más informativos y específicos a la aplicación.
RESPONSABILIDADES:
1. Extensión de Error: Añadir propiedades adicionales como código, título y tipo para proporcionar más contexto sobre el error.
2. Personalización de Errores: Permitir la creación de errores con información detallada y específica de la aplicación.
NOTAS:
Esta clase forma parte del sistema de gestión de errores de la biblioteca.
*/
class ErrorPersonalizado extends Error {
    constructor(plantilla, mensaje='', contexto={}, codigo=0) {
        super(mensaje);
        this.name = 'ErrorPersonalizado';
        this.plantilla = plantilla;
        this.contexto = contexto;
        this.codigo = codigo;
        this.tipo = Base.tipoDeMensaje(codigo);
    }
}

/* CLASE: ConfiguradorModulos
PROPOSITO: Administrar la configuración dinámica de los servicios que forman parte de la aplicación, proporcionando un mecanismo centralizado y modular para la gestión de configuraciones y la importación de extensiones de dichos servicios en tiempo de ejecución.
RESPONSABILIDADES:
1. Carga de Configuraciones: Carga y aplica la configuración específica de todos los servicios de la aplicación, basándose en los "esquema de servicio" que contiene los parámetros y datos de las configuraciones del servicio en formato JSON.
2. Extensión de Funcionalidades: Integra y extiende las funcionalidades de los servicios, importando dinámicamente las definiciones contenidas en las subclases de "DefinicionServicio" que sean creadas para cada uno de ellos como módulos JavaScript.
3. Gestión de Dependencias: Mapea las relaciones y dependencias entre diferentes componentes lógicos y funcionales de los servicios, para una correcta configuración y operación.
4. Inicialización de Servicios: Inicializa los servicios con las definiciones, extensiones y componentes cargados, asegurando que estén listos para su uso conforme a los requerimientos del contexto de la aplicación.
NOTAS:
Depende directamente de las subclases de los servicios, creadas como extensiones de "DefinicionServicio" (cuyas instancias se asignan a "definicionModulo"), las cuales proveen los contenidos específicos de las funciones y extensiones de cada servicio concreto.
Depende directamente del "esquema de servicio" que contiene los parámetros y datos de las configuraciones del servicio en formato JSON.
Interactúa con "CoordinadorGeneral" para disparar la configuración de servicios cuando se solicita su ejecución, y para entregarle el control del servicio una vez que se haya configurado.
*/
class ConfiguradorModulos {
    constructor() {
        this.gestorEstado = null;
        this.traductorIdiomas = null;
        this.definicionModulo = null;
        this.configuraciones = null;
        this._dominioTemporal = null;
        this._contenidoTemporal = '';
    }
    // Funciones privadas
    _inyectarExtensiones(coordinador) {
        try {
            coordinador.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('AccionesCoordinador'));
            coordinador.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('ReaccionesCoordinador'));
            coordinador.interfazUsuario.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('InterfazUsuario'));
            coordinador.interfazUsuario.presentadorContenido.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('PresentadorContenido'));
            coordinador.operadorDatos.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('OperadorDatos'));
            coordinador.operadorDatos.validadorDatos.inyectarValidadoresDatos(this.definicionModulo.traspasarDefiniciones('ValidadoresDatos'));
        } catch (error) {
            throw error;
        }
    }
    _extraerMapaInteracciones(coordinador, idServicio) {
        try {
            if (!this._dominioTemporal) { return; }
            coordinador.servicio = idServicio;
            if (!coordinador.INTERACCIONES[idServicio]) {
                coordinador.INTERACCIONES[idServicio] = new Map();
            }
            const capturarInteracciones = (conjuntoEsquemas) => {
                conjuntoEsquemas.forEach(esquema => {
                    if (esquema.interacciones) {
                        Object.keys(esquema.interacciones).forEach(key => {
                            const interaccion = esquema.interacciones[key];
                            if (interaccion.servicio === idServicio) {
                                coordinador.INTERACCIONES[idServicio].set(key, interaccion);
                            }
                        });
                    }
                    if (esquema.enlaces) {
                        Object.keys(esquema.enlaces).forEach(key => {
                            const enlace = esquema.enlaces[key];
                            if (enlace.servicio === idServicio) {
                                coordinador.INTERACCIONES[idServicio].set(key, enlace);
                            }
                        });
                    }
                });
            };
            if (this._dominioTemporal.formularios) capturarInteracciones(this._dominioTemporal.formularios);
            if (this._dominioTemporal.informes) capturarInteracciones(this._dominioTemporal.informes);
            if (this._dominioTemporal.navegacion && this._dominioTemporal.navegacion[idServicio]) {
                const navegacionServicio = this._dominioTemporal.navegacion[idServicio];
                Object.keys(navegacionServicio).forEach(key => {
                    const interaccion = navegacionServicio[key];
                    coordinador.INTERACCIONES[idServicio].set(key, interaccion);
                });
                if (this._dominioTemporal.navegacion.menus && this._dominioTemporal.navegacion.menus[idServicio]) {
                    const interaccionNavegacion = this._dominioTemporal.navegacion.menus[idServicio];
                    coordinador.INTERACCIONES[idServicio].set(idServicio, interaccionNavegacion);
                }
            }
        } catch (error) {
            throw error;
        }
    }
    async _cargarConfiguraciones(rutaEsquema) {
        try {
            const respuesta = await fetch(rutaEsquema);
            const esquemaServicio = await respuesta.json();
            if (!esquemaServicio) {
                throw new ErrorPersonalizado('ERROR_CARGAR_SERVICIO', '', {"ruta": rutaEsquema});
            }
            this.configuraciones = new Map();
            Object.entries(esquemaServicio).forEach(([clave, valor]) => {
                this.configuraciones.set(clave, valor);
            });
            return true;
        } catch (error) {
            throw error;
        }
    }
    _obtenerConfiguracion(clave) {
        return this.configuraciones.get(clave);
    }
    _configurarInteracciones(coordinador) {
        try {
            coordinador.interfazUsuario.inyectarExtensiones(this.definicionModulo.traspasarDefiniciones('ManejadoresInteracciones'));
            let funcionesInteraccion = {};
            const manejadoresInteracciones = this._obtenerConfiguracion('manejadoresInteracciones');
            if (!manejadoresInteracciones) {
                throw new ErrorPersonalizado('ERROR_MANEJADORES_EVENTOS');
            }
            for (const manejadorInteraccionUI of manejadoresInteracciones) {
                const { elemento, evento, manejador } = manejadorInteraccionUI;
                let identificador = `${elemento}:${evento}`;
                const funcionManejador = coordinador.interfazUsuario[manejador];
                if (typeof funcionManejador === 'function') {
                    funcionesInteraccion[identificador] = funcionManejador.bind(coordinador.interfazUsuario);
                } else {
                    throw new ErrorPersonalizado('ERROR_EXTENSION_NO_DEFINIDA', '', {"extension": manejador, "componente": "InterfazUsuario"});
                }
            }
            if (funcionesInteraccion) {
                for (let identificador in funcionesInteraccion) {
                    if (funcionesInteraccion.hasOwnProperty(identificador)) {
                        coordinador.interfazUsuario.MANEJADORES.set(identificador, funcionesInteraccion[identificador]);
                    }
                }
            }
            this._asignarManejadoresEventosUI(coordinador.interfazUsuario);
        } catch (error) {
            throw error;
        }
    }
    _definirAccionesCoordinador(coordinador) {
        try {
            const accionesCoordinador = this._obtenerConfiguracion('accionesCoordinador');
            if (!accionesCoordinador) {
                throw new ErrorPersonalizado('ERROR_ACCIONES_SERVICIO');
            }
            for (const accion of accionesCoordinador) {
                if (typeof coordinador[accion] === 'function') {
                    coordinador.interfazUsuario[accion] = coordinador[accion].bind(coordinador);
                } else {
                    throw new ErrorPersonalizado('ERROR_EXTENSION_NO_DEFINIDA', '', {"extension": accion, "componente": "CoordinadorGeneral"});
                }
            }
        } catch (error) {
            throw error;
        }
    }
    _definirReaccionesCoordinador(coordinador) {
        try {
            const suscripcionesCoordinador = this._obtenerConfiguracion('suscripcionesCoordinador');
            const indiceEventosModelo = this._obtenerConfiguracion('indiceEventosModelo');
            const indiceEventosVista = this._obtenerConfiguracion('indiceEventosVista');
            for (let identificador in suscripcionesCoordinador) {
                if (!suscripcionesCoordinador.hasOwnProperty(identificador)) continue;
                const reaccionCoordinador = suscripcionesCoordinador[identificador];
                if (typeof coordinador[reaccionCoordinador] !== 'function') {
                    throw new ErrorPersonalizado('ERROR_EXTENSION_NO_DEFINIDA', '', {"extension": reaccionCoordinador, "componente": "CoordinadorGeneral"});
                    //continue;
                }
                const eventoConfigurado = indiceEventosModelo[identificador] || indiceEventosVista[identificador];
                if (eventoConfigurado) {
                    coordinador.gestorEstado.notificadorEventos.suscribirEvento(
                        eventoConfigurado,
                        coordinador[reaccionCoordinador].bind(coordinador)
                    );
                }
            }
        } catch (error) {
            throw error;
        }
    }
    _definirReaccionesModelo(coordinador) {
        try {
            const suscripcionesOperadorDatos = this._obtenerConfiguracion('suscripcionesOperadorDatos');
            const indiceEventosModelo = this._obtenerConfiguracion('indiceEventosModelo');
            const indiceEventosVista = this._obtenerConfiguracion('indiceEventosVista');
            for (let identificador in suscripcionesOperadorDatos) {
                if (!suscripcionesOperadorDatos.hasOwnProperty(identificador)) continue;
                const reaccionModelo = suscripcionesOperadorDatos[identificador];
                if (typeof coordinador.operadorDatos[reaccionModelo] !== 'function') {
                    throw new ErrorPersonalizado('ERROR_EXTENSION_NO_DEFINIDA', '', {"extension": reaccionModelo, "componente": "OperadorDatos"});
                    //continue;
                }
                const eventoConfigurado = indiceEventosModelo[identificador] || indiceEventosVista[identificador];
                if (eventoConfigurado) {
                    coordinador.gestorEstado.notificadorEventos.suscribirEvento(
                        eventoConfigurado,
                        coordinador.operadorDatos[reaccionModelo].bind(coordinador.operadorDatos)
                    );
                }
            }
        } catch (error) {
            throw error;
        }
    }
    _definirReaccionesVista(coordinador) {
        try {
            const suscripcionesInterfazUsuario = this._obtenerConfiguracion('suscripcionesInterfazUsuario');
            const indiceEventosVista = this._obtenerConfiguracion('indiceEventosVista');
            const indiceEventosModelo = this._obtenerConfiguracion('indiceEventosModelo');
            for (let identificador in suscripcionesInterfazUsuario) {
                if (!suscripcionesInterfazUsuario.hasOwnProperty(identificador)) continue;
                const reaccionVista = suscripcionesInterfazUsuario[identificador];
                if (typeof coordinador.interfazUsuario[reaccionVista] !== 'function') {
                    throw new ErrorPersonalizado('ERROR_EXTENSION_NO_DEFINIDA', '', {"extension": reaccionVista, "componente": "InterfazUsuario"});
                    //continue;
                }
                const eventoConfigurado = indiceEventosVista[identificador] || indiceEventosModelo[identificador];
                if (eventoConfigurado) {
                    coordinador.gestorEstado.notificadorEventos.suscribirEvento(
                        eventoConfigurado,
                        coordinador.interfazUsuario[reaccionVista].bind(coordinador.interfazUsuario)
                    );
                }
            }
        } catch (error) {
            throw error;
        }
    }
    _definirOperacionesDatos(coordinador) {
        try {
            const operacionesDatos = this._obtenerConfiguracion('operacionesDatos');
            coordinador.operadorDatos.configurarOperaciones(operacionesDatos);
        } catch (error) {
            throw error;
        }
    }
    _asignarElementosUI(interfaz, vaciar=false) {
        const elementosUI = this.gestorEstado.obtenerValor(Base.Estados.vista, 'elementosUI');
        if (elementosUI) {
            if (vaciar) {interfaz.ELEMENTOS.clear();}
            for (let indice = 0; indice < elementosUI.length; indice++) {
                let clave = elementosUI[indice];
                let elemento = interfaz.manipuladorUI.seleccionar(`#${clave}`);
                if (elemento) {
                    interfaz.ELEMENTOS.set(clave, elemento);
                } else if (interfaz.ELEMENTOS.has(clave)) {
                    interfaz.ELEMENTOS.delete(clave);
                }
            }
        }
    }
    _asignarPlantillasUI(interfaz, contenedor='plantillas', reemplazar=false) {
        try {
            if (this._contenidoTemporal) {
                interfaz.presentadorContenido.agregarPlantillasContenedor(this._contenidoTemporal, contenedor, reemplazar);
                interfaz.presentadorContenido.autoregistrarPlantillas(contenedor);
                this._contenidoTemporal = '';
            }
        } catch (error) {
            throw error;
        }
    }
    _asignarManejadoresEventosUI(interfaz, vaciar=false) {
        if (vaciar) {
            this._eliminarManejadoresEventosUI(interfaz);
        }
        interfaz.MANEJADORES.forEach((manejador, identificador) => {
            const [selector, evento] = identificador.split(':');
            const elemento = interfaz.manipuladorUI.seleccionar(`#${selector}`);
            if (elemento) {
                interfaz.EVENTOS.set(`${selector}:${evento}`, manejador);
                interfaz.receptorUI.gestionarOyenteEvento(
                    'asignar', elemento, evento, manejador
                );
            }
        });
    }
    _eliminarManejadoresEventosUI(interfaz) {
        interfaz.EVENTOS.forEach((manejador, identificador) => {
            const [selector, evento] = identificador.split(':');
            const elemento = interfaz.manipuladorUI.seleccionar(`#${selector}`);
            if (elemento) {
                interfaz.receptorUI.gestionarOyenteEvento(
                    'eliminar', elemento, evento, manejador
                );
            }
        });
        interfaz.EVENTOS.clear();
    }
    async _cargarIdiomaUI(rutaIdioma, idiomaElegido) {
        try {
            await this.traductorIdiomas.cargarDesdeJson(rutaIdioma, idiomaElegido);
        } catch (error) {
            throw error;
        }
    }
    async _cargarPlantillasUI(rutaPlantillas) {
        try {
            const respuesta = await fetch(rutaPlantillas);
            if (!respuesta.ok) {
                throw new ErrorPersonalizado('ERROR_CARGAR_PLANTILLAS', respuesta.statusText, {"ruta": rutaPlantillas}, respuesta.status);
            }
            this._contenidoTemporal = await respuesta.text();
        } catch (error) {
            throw error;
        }
    }
    async _cargarEsquemasDominio(rutaEsquemas) {
        try {
            this._dominioTemporal = null;
            const respuesta = await fetch(rutaEsquemas);
            if (!respuesta.ok) { return; }
            this._dominioTemporal = await respuesta.json();
            if (!this._dominioTemporal) {
                throw new ErrorPersonalizado('ERROR_ESQUEMAS_NO_CARGADOS', '', {"ruta": rutaEsquemas});
            }
        } catch (error) {
            throw error;
        }
    }
    // Funciones públicas
    coordinarInicio(gestorEstado, traductorIdiomas) {
        Base.trazarFlujo(this.constructor.name, 'coordinarInicio', 2);
        if (typeof gestorEstado === 'object') {
            this.gestorEstado = gestorEstado;
            this.traductorIdiomas = traductorIdiomas;
        }
    }
    async importarModulo(rutaModulo) {
        Base.trazarFlujo(this.constructor.name, 'importarModulo', 2, rutaModulo);
        try {
            const noCache = new Date().getTime();
            const urlModulo = `${Base.construirUrlAbsoluta(rutaModulo)}?nocache=${noCache}`;
            const modulo = await import(urlModulo);
            this.definicionModulo = modulo.servicio;
            const rutaEsquema = urlModulo.replace('.js','.json');
            const resultadoCarga = await this._cargarConfiguraciones(rutaEsquema);
            if (resultadoCarga) {
                this.gestorEstado.asignarEstado(
                    Base.Estados.vista, 
                    this._obtenerConfiguracion('configuracionVista')
                );
                this.gestorEstado.asignarEstado(
                    Base.Estados.modelo, 
                    this._obtenerConfiguracion('configuracionModelo')
                );
                const rutaIdioma = this.gestorEstado.obtenerValor(Base.Estados.vista, 'rutaIdioma');
                const rutaPlantillas = this.gestorEstado.obtenerValor(Base.Estados.vista, 'rutaPlantillas');
                const idiomaElegido = this.gestorEstado.obtenerValor(Base.Estados.preferencias, 'idioma');
                const rutaDominio = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'rutaDominio');
                await this._cargarIdiomaUI(rutaIdioma, idiomaElegido);
                await this._cargarPlantillasUI(rutaPlantillas);
                await this._cargarEsquemasDominio(rutaDominio);
            }
        } catch (error) {
            throw error;
        }
    }
    aplicarConfiguracion(coordinador) {
        Base.trazarFlujo(this.constructor.name, 'aplicarConfiguracion', 2);
        try {
            const idServicio = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'idServicio');
            this._inyectarExtensiones(coordinador);
            this._extraerMapaInteracciones(coordinador, idServicio)
            this._configurarInteracciones(coordinador);
            this._asignarElementosUI(coordinador.interfazUsuario);
            this._asignarPlantillasUI(coordinador.interfazUsuario);
            this._definirAccionesCoordinador(coordinador);
            this._definirReaccionesCoordinador(coordinador);
            this._definirReaccionesModelo(coordinador);
            this._definirReaccionesVista(coordinador);
            this._definirOperacionesDatos(coordinador);
            this._contenidoTemporal = '';
            this._dominioTemporal = null;
            this.configuraciones = null;
            this.definicionModulo = null;
            return true;
        } catch (error) {
            throw error;
        }
    }
}

/* CLASE: InstaladorAplicacion
PROPOSITO: Gestionar el proceso de instalación y configuración inicial de la aplicación en el dispositivo del usuario como una Aplicación Web Progresiva (PWA). Su objetivo es proporcionar una interfaz clara y eficiente para instalar la aplicación, configurar aspectos esenciales y preparar el entorno para su primer uso.
RESPONSABILIDADES:
1. Gestión de la Instalación: Controla el proceso de instalación de la aplicación, incluyendo la 2. configuración de parámetros iniciales y la preparación del entorno.
2. Configuración Inicial: Establece valores y configuraciones iniciales requeridos para el correcto funcionamiento de la aplicación desde el primer uso.
3. Verificación de Requisitos: Comprueba la existencia y la adecuación del entorno y de las dependencias necesarias para la operación de la aplicación.
*/
class InstaladorAplicacion {
    constructor(gestorEstado, interfazUsuario, rutaErrores) {
        this.gestorEstado = gestorEstado;
        this.interfazUsuario = interfazUsuario;
        this.manejadorErrores = new ManejadorErrores(this.interfazUsuario.traductorIdiomas, rutaErrores);
        this.estaInstaladaPwa = false;
        this.estaSuscritoNotificaciones = false;
        this.trabajadorServicio = null;
    }
    // Funciones privadas
    async _enviarSuscripcionAlServidor(suscripcion) {
        const maxReintentos = 3;
        const { urlServidorSuscribir } = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'notificacionesPush');
        let intentos = 0;
        while (intentos < maxReintentos) {
            try {
                const respuesta = await fetch(urlServidorSuscribir, {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(suscripcion)
                });
                if (respuesta.ok) {
                    return await respuesta.json();
                } else {
                    throw new ErrorPersonalizado('ERROR_ENVIAR_SUSCRIPCION', respuesta.statusText, {"url": urlServidorSuscribir}, respuesta.status);
                }
            } catch (error) {
                if (intentos === maxReintentos - 1) {
                    throw error;
                }
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
            intentos++;
        }
    }
    async _notificarDesuscripcionAlServidor(suscripcion) {
        try {
            const { urlServidorDesuscribir } = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'notificacionesPush');
            const respuesta = await fetch(urlServidorDesuscribir, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(suscripcion)
            });
            if (respuesta.ok) {
                return respuesta.status === 200;
            } else {
                throw new ErrorPersonalizado('ERROR_NOTIFICAR_DESUSCRIPCION', respuesta.statusText, {"url": urlServidorDesuscribir}, respuesta.status);
            }
        } catch (error) {
            throw error;
        }
    }
    async _solicitarPermisoNotificaciones() {
        const autorizacion = await window.Notification.requestPermission();
        return autorizacion !== 'denied';
    }
    async _obtenerSuscripcionActual() {
        return await this.trabajadorServicio.pushManager.getSubscription();
    }
    async _crearNuevaSuscripcion() {
        const { clavePublicaServidor } = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'notificacionesPush');
        return await this.trabajadorServicio.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: Base.urlBase64Uint8Array(clavePublicaServidor)
        });
    }
    _manejarPermisoDenegado() {
        try {
            this.estaSuscritoNotificaciones = false;
            const opciones = {
                "visible": true,
                "activado": false,
                "etiqueta": this.interfazUsuario.traductorIdiomas._('NOTIFICACIONES_BLOQUEADAS'),
            };
            const botonSuscripcion = this.interfazUsuario.ELEMENTOS.get('boton_suscripcion');
            this.interfazUsuario.manipuladorUI.configurarElemento(botonSuscripcion, opciones);
        } catch (error) {
            throw error;
        }
    }
    _activarBotonSuscripcion() {
        try {
            this._actualizarBotonSuscripcion();
            const areaSuscripcion = this.interfazUsuario.ELEMENTOS.get('area_suscripcion');
            this.interfazUsuario.manipuladorUI.cambiarVisibilidad(areaSuscripcion, true, true);
        } catch (error) {
            throw error;
        }
    }
    _actualizarBotonSuscripcion() {
        try {
            const botonSuscripcion = this.interfazUsuario.ELEMENTOS.get('boton_suscripcion');
            if (this.estaSuscritoNotificaciones) {
                const opciones = {
                    "visible": true,
                    "activado": true,
                    "etiqueta": this.interfazUsuario.traductorIdiomas._('DESACTIVAR_NOTIFICACIONES'),
                };
                this.interfazUsuario.manipuladorUI.configurarElemento(botonSuscripcion, opciones, this.desuscribirNotificaciones.bind(this));
            } else {
                const opciones = {
                    "visible": true,
                    "activado": true,
                    "etiqueta": this.interfazUsuario.traductorIdiomas._('ACTIVAR_NOTIFICACIONES'),
                };
                this.interfazUsuario.manipuladorUI.configurarElemento(botonSuscripcion, opciones, this.suscribirNotificaciones.bind(this));
            }
        } catch (error) {
            throw error;
        }
    }
    _verificarInstalacionPwa() {
        this.estaInstaladaPwa = window.matchMedia('(display-mode: standalone)').matches;
        return this.estaInstaladaPwa;
    }
    _activarBotonInstalacion() {
        try {
            this._actualizarBotonInstalacion();
            const areaInstalacion = this.interfazUsuario.ELEMENTOS.get('area_instalacion');
            this.interfazUsuario.manipuladorUI.cambiarVisibilidad(areaInstalacion, true, true);
        } catch (error) {
            throw error;
        }
    }
    _actualizarBotonInstalacion() {
        try {
            const botonInstalacion = this.interfazUsuario.ELEMENTOS.get('boton_instalacion');
            if (this.estaInstaladaPwa) {
                const opciones = {
                    "visible": true,
                    "activado": false,
                    "etiqueta": this.interfazUsuario.traductorIdiomas._('APLICACION_INSTALADA'),
                };
                this.interfazUsuario.manipuladorUI.configurarElemento(botonInstalacion, opciones);
                const areaInstalacion = this.interfazUsuario.ELEMENTOS.get('area_instalacion');
                setTimeout( () => {
                    this.interfazUsuario.manipuladorUI.cambiarVisibilidad(areaInstalacion, false, true);
                }, 5000);
            } else {
                const opciones = {
                    "visible": true,
                    "activado": true,
                    "etiqueta": this.interfazUsuario.traductorIdiomas._('INSTALAR_APLICACION'),
                };
                this.interfazUsuario.manipuladorUI.configurarElemento(botonInstalacion, opciones, this.instalarAplicacion.bind(this));
            }
        } catch (error) {
            throw error;
        }
    }
    // Funciones de inicialización
    async inicializarTrabajadorServicio(urlTrabajadorServicio) {
        Base.trazarFlujo(this.constructor.name, 'inicializarTrabajadorServicio', 2, urlTrabajadorServicio);
        if ('serviceWorker' in navigator) {
            try {
                this.trabajadorServicio = await navigator.serviceWorker.register(urlTrabajadorServicio);
                this.gestorEstado.emitirEventoMensaje('CONFIRMACION_SW_REGISTRADO');
            } catch (error) {
                const errorProcesado = this.manejadorErrores.procesarError(error);
                this.gestorEstado.emitirEventoInformacion('ERROR_REGISTRAR_SW', errorProcesado);
            }
        }
    }
    inicializarInstalacion() {
        Base.trazarFlujo(this.constructor.name, 'inicializarInstalacion', 2);
        if ('serviceWorker' in navigator) {
            try {
                if (!this._verificarInstalacionPwa()) {
                    this._activarBotonInstalacion();
                }
            } catch (error) {
                const errorProcesado = this.manejadorErrores.procesarError(error);
                this.gestorEstado.emitirEventoInformacion('ERROR_INICIALIZAR_INSTALACION', errorProcesado);
            }
        }
    }
    inicializarSuscripcion() {
        Base.trazarFlujo(this.constructor.name, 'inicializarSuscripcion', 2);
        if ('serviceWorker' in navigator) {
            try {
                const { urlServidorSuscribir, urlServidorDesuscribir, clavePublicaServidor } = this.gestorEstado.obtenerValor(Base.Estados.modelo, 'notificacionesPush');
                const areaSuscripcion = this.interfazUsuario.ELEMENTOS.get('area_suscripcion');
                if (areaSuscripcion) {
                    if (navigator.serviceWorker.controller) {
                        navigator.serviceWorker.controller.postMessage({
                            clavePublicaServidor: clavePublicaServidor,
                            urlServidorSuscribir: urlServidorSuscribir,
                            urlServidorDesuscribir: urlServidorDesuscribir
                        });
                    }
                    navigator.serviceWorker.addEventListener('message', evento => {
                        if (evento.data && evento.data.type === 'NOTIFICATION_RECEIVED') {
                            this.gestorEstado.emitirEventoMensaje('NOTIFICACION_PUSH_RECIBIDA', '', Base.Mensajes.AVISO, evento.data);
                        }
                    });
                    this._activarBotonSuscripcion();
                }
            } catch (error) {
                const errorProcesado = this.manejadorErrores.procesarError(error);
                this.gestorEstado.emitirEventoInformacion('ERROR_INICIALIZAR_SUSCRIPCION', errorProcesado);
            }
        }
    }
    // Funciones para manejo de Notificaciones push
    async suscribirNotificaciones() {
        Base.trazarFlujo(this.constructor.name, 'suscribirNotificaciones', 2);
        try {
            if (!await this._solicitarPermisoNotificaciones()) {
                this._manejarPermisoDenegado();
                return;
            }
            const suscripcionActual = await this._obtenerSuscripcionActual();
            if (suscripcionActual) {
                this.estaSuscritoNotificaciones = true;
                this._actualizarBotonSuscripcion();
                return suscripcionActual;
            }
            const nuevaSuscripcion = await this._crearNuevaSuscripcion();
            if (!nuevaSuscripcion) return;
            const suscripcionEnviada = await this._enviarSuscripcionAlServidor(nuevaSuscripcion);
            if (!suscripcionEnviada) {
                throw new ErrorPersonalizado('ERROR_SUSCRIBIR_NOTIFICACIONES');
            }
            this.gestorEstado.emitirEventoMensaje('CONFIRMACION_SUSCRIPCION_NOTIFICACIONES', this.interfazUsuario.traductorIdiomas._('SUSCRIPCION_EXITOSA'), Base.Mensajes.EXITO);
            this.estaSuscritoNotificaciones = true;
            this._actualizarBotonSuscripcion();
            return suscripcionEnviada;
        } catch (error) {
            const errorProcesado = this.manejadorErrores.procesarError(error);
            this.gestorEstado.emitirEventoInformacion('ERROR_SUSCRIBIR_NOTIFICACIONES', errorProcesado);
        }
    }
    async desuscribirNotificaciones() {
        Base.trazarFlujo(this.constructor.name, 'desuscribirNotificaciones', 2);
        try {
            const suscripcion = await this.trabajadorServicio.pushManager.getSubscription();
            if (!suscripcion) return;
            const resultadoDesuscripcion = await suscripcion.unsubscribe();
            if (!resultadoDesuscripcion) {
                throw new ErrorPersonalizado('ERROR_DESUSCRIBIR_NOTIFICACIONES');
            }
            const notificacionEnviada = await this._notificarDesuscripcionAlServidor(suscripcion);
            if (!notificacionEnviada) {
                return;
            }
            this.gestorEstado.emitirEventoMensaje('CONFIRMACION_DESUSCRIPCION_NOTIFICACIONES', this.interfazUsuario.traductorIdiomas._('DESUSCRIPCION_EXITOSA'), Base.Mensajes.EXITO);
            this.estaSuscritoNotificaciones = false;
            this._actualizarBotonSuscripcion();
        } catch (error) {
            const errorProcesado = this.manejadorErrores.procesarError(error);
            this.gestorEstado.emitirEventoInformacion('ERROR_DESUSCRIBIR_NOTIFICACIONES', errorProcesado);
        }
    }
    // Funciones para instalación de la Aplicación (PWA)
    async instalarAplicacion() {
        Base.trazarFlujo(this.constructor.name, 'instalarAplicacion', 2);
        try {
            if (!window.promptInstalacion) {
                throw new ErrorPersonalizado('SIN_INSTALACION_PENDIENTE');
            }
            window.promptInstalacion.prompt();
            const { outcome } = await window.promptInstalacion.userChoice;
            if (outcome === 'accepted') {
                this.gestorEstado.emitirEventoMensaje('CONFIRMACION_PWA_INSTALADA', this.interfazUsuario.traductorIdiomas._('INSTALACION_EXITOSA'), Base.Mensajes.EXITO);
                this.estaInstaladaPwa = true;
                this._actualizarBotonInstalacion();
            } else {
                this.gestorEstado.emitirEventoMensaje('INSTALACION_RECHAZADA_POR_USUARIO', this.interfazUsuario.traductorIdiomas._('INSTALACION_RECHAZADA'), Base.Mensajes.ALERTA);
                this.estaInstaladaPwa = false;
                this._actualizarBotonInstalacion();
                const areaInstalacion = this.interfazUsuario.ELEMENTOS.get('area_instalacion');
                this.interfazUsuario.manipuladorUI.cambiarVisibilidad(areaInstalacion, false, true);
            }
        } catch (error) {
            const errorProcesado = this.manejadorErrores.procesarError(error);
            this.gestorEstado.emitirEventoInformacion('ERROR_INSTALAR_PWA', errorProcesado);
        }
    }
}

/* **************************************************************************** */
/* CLASES DEL AMBITO "GLOBAL" */

/* CLASE: GestorEstado [singleton]
PROPOSITO: Mantener y gestionar el estado compartido en toda la aplicación, actuando como un repositorio centralizado para la información que puede ser utilizada, modificada y sincronizada por los diferentes servicios, capas y componentes del sistema, y proporcionando un punto de acceso unificado y coherente para ello.
RESPONSABILIDADES:
1. Centralización del Estado: Almacena el estado global de la aplicación, incluyendo configuraciones, datos de sesión, preferencias de usuario, datos temporales de las operaciones, y cualquier otro dato relevante que necesite ser compartido entre diferentes partes de la aplicación, ofreciendo además mecanismos para guardar y cargar el estado desde el almacenamiento local.
2. Gestión de Cambios de Estado: Ofrece una API interna sencilla para actualizar y consultar el mapa del estado global de la aplicación, garantizando la coherencia y actualización oportuna de la información.
3. Integración con Sistema de Publicación/Suscripción: Automatiza las notificaciones de cambios en el estado global a los diversos componentes que se encuentren suscritos, y provee mecanismos para que todos ellos puedan actuar también como publicadores y emitir sus propios eventos de cambio. 
4. Interacción con Otros Componentes: Sirve como puente para que otras clases instanciadas en la aplicación accedan y modifiquen el estado global según sea necesario, y puedan también intercambiar y traspasar globalmente información relevante entre ellas.
NOTAS:
Interactúa con varias clases de la aplicación, ya que proporciona el estado necesario para que éstas funcionen correctamente:
- InterfazUsuario.
- OperadorDatos (y sus complementos ComunicadorApi, CreadorAdaptadoresApi, AdaptadorApi y todas sus subclases).
- CoordinadorGeneral (junto con PortadorInformacion, ConfiguradorModulos e InstaladorAplicacion).
- Todas las subclases de servicios derivadas de DefinicionServicio (que es donde realmente se programan las extensiones de los servicios desarrollados).
*/
class GestorEstado {
    constructor(almacenamientoLocal='estadosApp', notificadorEventos=null) {
        this.notificadorEventos = notificadorEventos || new NotificadorEventos();
        this.nombreAlmacenamientoLocal = almacenamientoLocal;
        this.ESTADOS = null;
        this._cargarEstado();
    }
    static obtenerInstancia(almacenamientoLocal='estadosApp', notificadorEventos=null) {
        if (!this.instancia) {
            this.instancia = new GestorEstado(almacenamientoLocal, notificadorEventos);
        }
        return this.instancia;
    }
    // Funciones privadas
    _establecerValoresIniciales() {
        this.ESTADOS.get(Base.Estados.preferencias).set('tiempoVisor', 5);
        this.ESTADOS.get(Base.Estados.preferencias).set('idioma', 'es');
    }
    _cargarEstado() {
        const estadoGuardado = localStorage.getItem(this.nombreAlmacenamientoLocal);
        this.ESTADOS = new Map();
        if (estadoGuardado) {
            const estadoObj = JSON.parse(estadoGuardado);
            Object.entries(estadoObj).forEach(([clave, valor]) => {
                this.ESTADOS.set(clave, valor instanceof Object && !(valor instanceof Array) ? new Map(Object.entries(valor)) : valor);
            });
        } else {
            this.ESTADOS.set(Base.Estados.sesion, new Map());
            this.ESTADOS.set(Base.Estados.preferencias, new Map());
            this.ESTADOS.set(Base.Estados.vista, new Map());
            this.ESTADOS.set(Base.Estados.modelo, new Map());
            this.ESTADOS.set(Base.Estados.aplicacion, new Map());
            this.ESTADOS.set(Base.Estados.memoria, new Map());
            this._establecerValoresIniciales();
        }
    }
    _guardarEstado() {
        const estadoParaGuardar = {};
        this.ESTADOS.forEach((valor, clave) => {
            estadoParaGuardar[clave] = valor instanceof Map ? Object.fromEntries(valor) : valor;
        });
        localStorage.setItem(this.nombreAlmacenamientoLocal, JSON.stringify(estadoParaGuardar));
    }
    _vaciarEstado(grupo='*') {
        if (grupo === '*') {
            this.ESTADOS.clear();
        } else {
            if (this.ESTADOS.has(grupo)) {
                this.ESTADOS.delete(grupo)
            }
        }
        this._guardarEstado();
        this._cargarEstado();
    }
    // Funciones para Estado global
    obtenerEstado(grupo='*') {
        Base.trazarFlujo(this.constructor.name, 'obtenerEstado', 4, `grupo=${grupo}`);
        if (grupo === '*') {
            return this.ESTADOS;
        } else {
            return this.ESTADOS.get(grupo);
        }
    }
    actualizarEstado(nombreEvento, grupo, valores, guardar=false) {
        Base.trazarFlujo(this.constructor.name, 'actualizarEstado', 3, nombreEvento, `grupo=${grupo}`, `guardar=${guardar}`);
        if (this.asignarEstado(grupo, valores)) {
            const datosEvento = {
                "cambio": nombreEvento,
                "grupo": grupo,
                "valores": this.obtenerEstado(grupo)
            };
            if (guardar) {
                this._guardarEstado();
            }
            if (nombreEvento) {
                this.notificadorEventos.notificarCambio(nombreEvento, datosEvento);
            }
        }
    }
    asignarEstado(grupo, valores) {
        Base.trazarFlujo(this.constructor.name, 'asignarEstado', 4, `grupo=${grupo}`);
        const grupoEstado = this.ESTADOS.get(grupo);
        if (!grupoEstado) {
            console.error(`El grupo "${grupo}" no existe en el estado global.`);
            return false;
        }
        if (valores instanceof Map) {
            this.ESTADOS.set(grupo, new Map(valores));
        } else if (typeof valores === 'object' && valores !== null) {
            const valoresMap = new Map(Object.entries(valores));
            this.ESTADOS.set(grupo, valoresMap);
        } else if (valores === null) {
            grupoEstado.clear();
        } else {
            console.error(`Tipo de "valores" no soportado en el grupo "${grupo}".`);
            return false;
        }
        return true;
    }
    // Funciones para valores de Estado
    actualizarValores(nombreEvento, grupo, valores={}, guardar=false) {
        Base.trazarFlujo(this.constructor.name, 'actualizarValores', 3, nombreEvento, `grupo=${grupo}`, `guardar=${guardar}`);
        if (typeof valores === 'object' && grupo && this.ESTADOS.has(grupo) && this.ESTADOS.get(grupo) instanceof Map) {
            const grupoEstado = this.ESTADOS.get(grupo);
            Object.entries(valores).forEach(([clave, valor]) => {
                grupoEstado.set(clave, valor);
            });
            const datosEvento = {
                "cambio": nombreEvento,
                "grupo": grupo,
                "valores": Object.fromEntries(grupoEstado)
            };
            if (guardar) {
                this._guardarEstado();
            }
            if (nombreEvento) {
                this.notificadorEventos.notificarCambio(nombreEvento, datosEvento);
            }
        }
    }
    actualizarValor(nombreEvento, grupo, clave, valor, guardar=false) {
        Base.trazarFlujo(this.constructor.name, 'actualizarValor', 3, `${grupo} / ${clave}=${valor}`, `guardar=${guardar}`);
        if (this.ESTADOS.has(grupo) && this.ESTADOS.get(grupo) instanceof Map) {
            this.ESTADOS.get(grupo).set(clave, valor);
            const datosEvento = {
                "cambio": nombreEvento,
                "grupo": grupo,
                "clave": clave,
                "valor": valor
            };
            if (guardar) {
                this._guardarEstado();
            }
            if (nombreEvento) {
                this.notificadorEventos.notificarCambio(nombreEvento, datosEvento);
            }
        }
    }
    obtenerValor(grupo, clave) {
        Base.trazarFlujo(this.constructor.name, 'obtenerValor', 3, `${grupo} / ${clave}`);
        if (this.ESTADOS.has(grupo)) {
            if (this.ESTADOS.get(grupo).has(clave)) {
                return this.ESTADOS.get(grupo).get(clave);
            }
        }
        return null;
    }
    asignarValor(grupo, clave, valor) {
        Base.trazarFlujo(this.constructor.name, 'asignarValor', 3, `${grupo} / ${clave}=${valor}`);
        if (this.ESTADOS.has(grupo)) {
            this.ESTADOS.get(grupo).set(clave, valor);
        }
    }
    // Funciones para eventos de cambios de estado
    emitirEventoMensaje(nombreEvento, textoMensaje='', tipoMensaje=Base.Mensajes.AVISO, valores={}, codigo=0) {
        Base.trazarFlujo(this.constructor.name, 'emitirEventoMensaje', 3, nombreEvento);
        let datosEvento = {};
        if (tipoMensaje || valores) {
            datosEvento = this.notificadorEventos.empaquetarMensaje({
                'mensaje': textoMensaje,
                'tipo': tipoMensaje,
                'valores': valores,
                'codigo': codigo
            });
        }
        this.notificadorEventos.notificarCambio(nombreEvento, datosEvento);
    }
    emitirEventoInformacion(nombreEvento, datosEvento) {
        Base.trazarFlujo(this.constructor.name, 'emitirEventoInformacion', 3, nombreEvento);
        this.notificadorEventos.notificarCambio(nombreEvento, datosEvento);
    }
    // Funciones especiales para Grupos
    leerPreferenciaUsuario(clave, predeterminado) {
        Base.trazarFlujo(this.constructor.name, 'leerPreferenciaUsuario', 3, clave);
        let valor = this.ESTADOS.get(Base.Estados.preferencias).get(clave) || null;
        if (!valor && predeterminado) {
            valor = predeterminado;
        }
        return valor;
    }
    establecerPreferenciaUsuario(clave, valor) {
        Base.trazarFlujo(this.constructor.name, 'establecerPreferenciaUsuario', 3, `${clave}=${valor}`);
        if (clave && valor) {
            this.ESTADOS.get(Base.Estados.preferencias).set(clave, valor);
            return valor;
        }
        return null;
    }
}

/* CLASE: NotificadorEventos
PROPOSITO: Gestionar la suscripción y la notificación de eventos, tanto de la capa de Modelo como de la capa de Vista, dentro de un esquema multi-direccional "muchos-a-muchos". Esta clase facilita la implementación de una comunicación más directa, dinámica y desacoplada entre las capas, permitiendo una gran variedad de interacciones y flujos de datos.
RESPONSABILIDADES:
1. Gestionar Suscripciones a Eventos: Permite que cualquier componente principal de la biblioteca (como CoordinadorGeneral, OperadorDatos o InterfazUsuario) se suscriba a eventos específicos, ya sean eventos de Modelo o de Vista.
2. Manejo de Eventos: Una vez que un evento es publicado (notificado) por cualquier componente, esta clase es responsable de invocar las funciones o manejadores de eventos suscritos, facilitando la respuesta y el manejo de estos eventos en tiempo real.
3. Facilitar la Comunicación Directa y Dinámica: La clase permite una comunicación más fluida y directa entre las diferentes capas de la aplicación, sin la necesidad de depender exclusivamente del Presentador como intermediario.
NOTAS:
Al permitir que tanto el Presentador, la Vista y el Modelo actúen como publicadores y suscriptores ofrece una gran flexibilidad en la gestión de eventos, adaptándose a una amplia gama de necesidades y escenarios de aplicación.
Su capacidad para manejar un esquema multi-direccional de publicación/suscripción "muchos-a-muchos" facilita la implementación de patrones arquitectónicos más complejos y dinámicos, como el MVVM.
Es la base para implementar una arquitectura reactiva y desacoplada, donde los distintos componentes puedan reaccionar a eventos sin depender directamente unos de otros.
El uso efectivo de esta clase depende de los "Undices de Eventos" disponibles en el "esquema de configuracion" de cada servicio de aplicación (en las definiciones de indiceEventosModelo y indiceEventosVista).
Las personalización de las suscripciones a los eventos dentro de cada servicio se registra en su respectiva configuración en el esquema del servicio (en las definiciones de suscripcionesInterfazUsuario y suscripcionesOperadorDatos).
*/
class NotificadorEventos {
    constructor() {
        this.SUSCRIPTORES = [];
    }
    suscribirEvento(nombreEvento, suscriptor) {
        Base.trazarFlujo(this.constructor.name, 'suscribirEvento', 4, nombreEvento);
        if (!this.SUSCRIPTORES[nombreEvento]) {
            this.SUSCRIPTORES[nombreEvento] = [];
        }
        this.SUSCRIPTORES[nombreEvento].push(suscriptor);
    }
    notificarCambio(nombreEvento, datosEvento) {
        Base.trazarFlujo(this.constructor.name, 'notificarCambio', 4, datosEvento);
        if (nombreEvento && this.SUSCRIPTORES[nombreEvento]) {
            this.SUSCRIPTORES[nombreEvento].forEach(suscriptor => suscriptor(datosEvento));
        }
    }
    empaquetarMensaje(parametros) {
        if (typeof parametros === 'object') {
            const { mensaje, tipo, codigo, valores } = parametros;
            return {
                'tipo': tipo,
                'mensaje': mensaje,
                'codigo': codigo, 
                'valores': valores
            };
        }
    }
}

/* CLASE: Base (estática)
PROPOSITO: Proveer un repositorio centralizado para valores constantes y configuraciones fijas que se utilizan en toda la aplicación, manteniendo un único punto de referencia para valores que no cambian durante la ejecución del programa y garantizando con ello la coherencia y facilidad de mantenimiento.
RESPONSABILIDADES:
1. Almacenamiento de Valores Constantes: Contiene definiciones de constantes utilizadas en múltiples partes de la aplicación, como códigos de error, tipos de archivos, tipos de mensajes y valores predeterminados, entre otros.
2. Facilitación del Mantenimiento y Cambios: Permite actualizar valores constantes en un solo lugar, evitando la necesidad de hacer cambios dispersos por todo el código.
3. Mejora de la Legibilidad del Código: Hace que el código sea más legible y entendible al reemplazar "números mágicos" y cadenas literales con nombres de constantes descriptivos.
NOTAS:
Es utilizada por prácticamente todas las clases de la aplicación, y su implementación es crítica para garantizar la cohesión y la consistencia en el manejo de valores fijos y configuraciones a lo largo de la aplicación.
*/
class Base {
    static formatosDeFecha(cadenaFecha=null) {
        let fechaHora = new Date();
        if (cadenaFecha) {
            fechaHora = new Date(cadenaFecha);
            if (isNaN(fechaHora.getTime())) {
                fechaHora = new Date();
            }
        }
        const ano = fechaHora.getFullYear();
        const mes = (fechaHora.getMonth() + 1).toString().padStart(2, '0');
        const dia = fechaHora.getDate().toString().padStart(2, '0');
        const hora = fechaHora.getHours().toString().padStart(2, '0');
        const minuto = fechaHora.getMinutes().toString().padStart(2, '0');
        const segundo = fechaHora.getSeconds().toString().padStart(2, '0');
        return {
            amd: `${ano}-${mes}-${dia}`,
            dma: `${dia}-${mes}-${ano}`,
            mda: `${mes}-${dia}-${ano}`,
            md: `${mes}-${dia}`,
            dm: `${dia}-${mes}`,
            am: `${ano}-${mes}`,
            ma: `${mes}-${ano}`,
            dia: `${dia}`,
            mes: `${mes}`,
            ano: `${ano}`,
            periodo: `${ano}${mes}${dia}`,
            horas: `${hora}`,
            minutos: `${minuto}`,
            segundos: `${segundo}`,
            hm: `${hora}:${minuto}`,
            hms: `${hora}:${minuto}:${segundo}`,
            todo: `${ano}${mes}${dia}${hora}${minuto}${segundo}`
        };
    }
    static fechaEnFormato(cadenaFecha=null, formato='dma') {
        const fechaHora = new Date(cadenaFecha);
        if (isNaN(fechaHora.getTime())) {
            return '';
        }
        const ano = fechaHora.getFullYear();
        const mes = (fechaHora.getMonth() + 1).toString().padStart(2, '0');
        const dia = fechaHora.getDate().toString().padStart(2, '0');
        const hora = fechaHora.getHours().toString().padStart(2, '0');
        const minuto = fechaHora.getMinutes().toString().padStart(2, '0');
        const segundo = fechaHora.getSeconds().toString().padStart(2, '0');
        switch (formato) {
            case 'amd':
                return `${ano}-${mes}-${dia}`;
            case 'dma':
                return `${dia}-${mes}-${ano}`;
            case 'mda':
                return `${mes}-${dia}-${ano}`;
            case 'md':
                return `${mes}-${dia}`;
            case 'periodo':
                return `${ano}${mes}${dia}`;
            case 'hora':
                return `${hora}:${minuto}`;
            case 'todo':
                return `${ano}${mes}${dia}${hora}${minuto}${segundo}`;
            default:
                return '';
        }
    }
    static tipoDeMensaje(estado) {
        if (estado < 200) return Base.Mensajes.ERROR;
        if (estado < 300) return Base.Mensajes.EXITO;
        if (estado < 400) return Base.Mensajes.AVISO;
        if (estado < 500) return Base.Mensajes.ALERTA;
        return Base.Mensajes.ERROR;
    }
    static tipoDeArchivo(tipo) {
        return Base.archivos[tipo];
    }
    static atributoTipoArchivo(tipo, atributo) {
        const tipoArchivo = Base.archivos[tipo];
        return tipoArchivo ? tipoArchivo[atributo] : null;
    }
    static construirUrlAbsoluta(rutaRelativa) {
        let urlAbsoluta;
        if (rutaRelativa.startsWith('/')) {
            urlAbsoluta = new URL(rutaRelativa, window.location.origin).href;
        } else {
            const pathCompleto = window.location.pathname;
            const pathBase = pathCompleto.substring(0, pathCompleto.lastIndexOf('/'));
            urlAbsoluta = new URL(rutaRelativa, `${window.location.origin}${pathBase}/`).href;
        }
        return urlAbsoluta;
    }
    static urlBase64Uint8Array(cadenaBase64) {
        const padding = '='.repeat((4 - cadenaBase64.length % 4) % 4);
        const base64 = (cadenaBase64 + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
    static generarUUID() {
        const timestamp = new Date().getTime();
        const highResolutionTime = (typeof performance !== 'undefined' && performance.now && performance.now() * 1000) || 0;
        let currentOffset = timestamp || highResolutionTime;
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const randomValue = Math.random() * 16;
            const value = (currentOffset + randomValue) % 16 | 0;
            currentOffset = Math.floor(currentOffset / 16);
            return (c === 'x' ? value : (value & 0x3 | 0x8)).toString(16);
        });
    }
    static reemplazarMarcadores(contenido, marcadores) {
        if (marcadores) {
            for (let clave in marcadores) {
                contenido = contenido.replace(new RegExp(`\\(\\(${clave}\\)\\)`, 'g'), marcadores[clave]);
            }
        }
        return contenido;
    }
    static desencriptarTexto(textoCifrado, claveCifrado) {
        textoCifrado = atob(textoCifrado);
        let resultado = '';
        for (let i = 0; i < textoCifrado.length; i++) {
            resultado += String.fromCharCode(textoCifrado.charCodeAt(i) ^ claveCifrado.charCodeAt(i % claveCifrado.length));
        }
        return resultado;
    }
    static cadenaUrl(url) {
        url = url.replace('http://', '').replace('https://', '');
        url = url.replace(/[\s/.]/g, '');
        return url.replace(/[^\x00-\x7F]/g, '');
    }
    static trazarFlujo(clase, funcion, nivel, ...args) {
        if (typeof nivel_trazado === 'undefined' || typeof filtro_trazado == 'undefined') return;
        if (!nivel || nivel_trazado < nivel) return;
        if (filtro_trazado && filtro_trazado.length > 0 && !filtro_trazado.includes(clase)) return;
        const argsLegibles = args.map(arg => {
            if (typeof arg === 'object') {
                try {
                    return JSON.stringify(arg, null, 2);
                } catch (e) {
                    return 'ERROR';
                }
            } else if (typeof arg === 'function') {
                return 'FUNCION';
            }
            return `${arg}`;
        });
        let imprimir = `${nivel} ${clase}.${funcion}`;
        if (argsLegibles && argsLegibles.length > 0) {
            imprimir += `: ${argsLegibles.join(' | ')}`;
        }
        console.log(imprimir);
    }
    static mostrarInformacion(coordinador, informacion) {
        const mapeoInformacion = {
            'interacciones': () => ({"CoordinadorGeneral.INTERACCIONES": coordinador.INTERACCIONES}),
            'historial': () => ({"CoordinadorGeneral.HISTORIAL": coordinador.HISTORIAL}),
            'operaciones': () => ({"OperadorDatos.OPERACIONES": coordinador.operadorDatos.OPERACIONES}),
            'estados': () => ({"GestorEstado.ESTADOS": coordinador.gestorEstado.ESTADOS}),
            'suscriptores': () => ({"NotificadorEventos.SUSCRIPTORES": coordinador.gestorEstado.notificadorEventos.SUSCRIPTORES}),
            'registros': () => ({"RegistradorErrores.REGISTROS": coordinador.manejadorErrores.registradorErrores.REGISTROS}),
            'textos': () => ({"TraductorIdiomas.TEXTOS": coordinador.interfazUsuario.traductorIdiomas.TEXTOS}),
            'elementos': () => ({"InterfazUsuario.ELEMENTOS": coordinador.interfazUsuario.ELEMENTOS}),
            'plantillas': () => ({"InterfazUsuario.PLANTILLAS": coordinador.interfazUsuario.PLANTILLAS}),
            'eventos': () => ({"InterfazUsuario.EVENTOS": coordinador.interfazUsuario.EVENTOS}),
            'manejadores': () => ({"InterfazUsuario.MANEJADORES": coordinador.interfazUsuario.MANEJADORES}),
            'componentes': () => ({"AdaptadorUI.COMPONENTES": coordinador.interfazUsuario.adaptadorUI.COMPONENTES})
        };
        console.log(mapeoInformacion[informacion] ? mapeoInformacion[informacion]() : null);
    }
    static Mensajes = class {
        static get EXITO() { return 'success'; }
        static get AVISO() { return 'info'; }
        static get ALERTA() { return 'warning'; }
        static get ERROR() { return 'danger'; }
    }
    static Errores = class {
        static get NO_VALIDO() { return 400; }
        static get NO_AUTENTICADO() { return 401; }
        static get NO_AUTORIZADO() { return 403; }
        static get NO_ENCONTRADO() { return 404; }
        static get NO_PERMITIDO() { return 405; }
        static get NO_CONTINUADO() { return 410; }
        static get NO_SOPORTADO() { return 415; }
        static get NO_PROCESABLE() { return 422; }
        static get NO_ATENDIDO() { return 429; }
        static get NO_REALIZADO() { return 500; }
        static get NO_DISPONIBLE() { return 503; }
    }
    static Estados = class {
        static get sesion() { return 'sesion'; }
        static get preferencias() { return 'preferencias'; }
        static get vista() { return 'vista'; }
        static get modelo() { return 'modelo'; }
        static get aplicacion() { return 'aplicacion'; }
        static get memoria() { return 'memoria'; }
    }
    static archivos = {
        HTML: { formato: "HTML", extension: "html", mime: "text/html" },
        MANIFEST: { formato: "MANIFEST", extension: "json", mime: "application/manifest+json" },
        JSON: { formato: "JSON", extension: "json", mime: "application/json" },
        TXT: { formato: "TXT", extension: "txt", mime: "text/plain" },
        BIN: { formato: "BIN", extension: "bin", mime: "application/octet-stream" },
        CSV: { formato: "CSV", extension: "csv", mime: "text/csv" },
        JPG: { formato: "JPG", extension: "jpg", mime: "image/jpeg" },
        PNG: { formato: "PNG", extension: "png", mime: "image/png" },
        JS: { formato: "JS", extension: "js", mime: "text/javascript" },
        PDF: { formato: "PDF", extension: "pdf", mime: "application/pdf" },
        XML: { formato: "XML", extension: "xml", mime: "application/xml" },
        XHTML: { formato: "XHTML", extension: "xhtml", mime: "application/xhtml+xml" },
        ZIP: { formato: "ZIP", extension: "zip", mime: "application/zip" },
        XLS: { formato: "XLS", extension: "xls", mime: "application/vnd.ms-excel" },
        XLSX: { formato: "XLSX", extension: "xlsx", mime: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" },
        DOC: { formato: "DOC", extension: "doc", mime: "application/msword" },
        DOCX: { formato: "DOCX", extension: "docx", mime: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
        PPT: { formato: "PPT", extension: "ppt", mime: "application/vnd.ms-powerpoint" },
        PPTX: { formato: "PPTX", extension: "pptx", mime: "application/vnd.openxmlformats-officedocument.presentationml.presentation" },
        MP3: { formato: "MP3", extension: "mp3", mime: "audio/mpeg" },
        MP4: { formato: "MP4", extension: "mp4", mime: "video/mpeg" },
        OPUS: { formato: "OPUS", extension: "opus", mime: "audio/opus" },
        WEBM: { formato: "WEBM", extension: "webm", mime: "video/webm" },
        WEBA: { formato: "WEBA", extension: "weba", mime: "audio/webm" },
        OGG: { formato: "OGG", extension: "ogg", mime: "audio/ogg" },
        WAV: { formato: "WAV", extension: "wav", mime: "audio/wav" },
        SVG: { formato: "SVG", extension: "svg", mime: "image/svg+xml" }
    };
    static textosUI = {
        "ERROR_CARGAR_MANIFIESTO": "Error al cargar maniifiesto de la aplicación desde '((url))': ((respuesta))",
        "ERROR_CARGAR_SERVICIO": "No se cargó el esquema del servicio en '((ruta))'",
        "ERROR_CARGAR_IDIOMA": "Error al cargar esquema de idioma '((ruta))': ((respuesta))",
        "ERROR_ENVIAR_DATOS": "Error en los datos enviados: ((respuesta))",
        "ERROR_CARGAR_PLANTILLAS": "Error al cargar plantillas de vistas desde '((ruta))': ((respuesta))",
        "ERROR_ESQUEMAS_NO_CARGADOS": "Error al cargar los esquemas desde la ruta '((ruta))'",
        "ERROR_MANEJADORES_EVENTOS": "No hay manejadores de eventos para la UI",
        "ERROR_EXTENSION_NO_DEFINIDA": "Extensión '((extension))' no definida en '((componente))'",
        "ERROR_ACCIONES_SERVICIO": "No hay acciones definidas para el servicio",
        "ERROR_FORMULARIO_NO_VALIDO": "El formulario contiene datos no válidos"
    };
}
