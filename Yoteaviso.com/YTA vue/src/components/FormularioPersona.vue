<template>

  <div id="formulario-persona">
    <form @submit.prevent="enviarFormulario" >
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <label>Nombre</label>
              <input 
              ref = "nombre"
              v-model="persona.nombre"
              type="text" 
              class="form-control"
              :class ="{'is-invalid': procesando && nombreInvalido }"
              @focus="resetEstado"
              @keypress="resetEstado"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Apellido</label>
              <input 
              v-model="persona.apellido" 
              type="text" 
              class="form-control"
              :class ="{'is-invalid': procesando && apellidoInvalido }"
               />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Email</label>
              <input v-model="persona.email" 
              type="email" 
              class="form-control"
              :class ="{'is-invalid': procesando && emailInvalido }" 
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Numero</label>
              <input v-model="persona.numero" 
              type="tel" 
              class="form-control"
              :class ="{'is-invalid': procesando && numeroInvalido }" 
              />
            </div>
          </div>
           <div class="col-md-4">
            <div class="form-group">
              <label>Precio alerta</label>
              <input 
              v-model="persona.precioalerta" 
              type="float" 
              class="form-control"
              :class ="{'is-invalid': procesando && numeroInvalido }"
               />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Link</label>
              <input 
              v-model="persona.link" 
              type="text" 
              class="form-control"
              :class ="{'is-invalid': procesando && linkInvalido }"
               />
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <button class="btn btn-primary">Crea tu alerta</button>
            </div>
          </div>
        </div>
      </div>
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div v-if="error && procesando" class="alert
          alert-danger" role="alert">
            Debes rellenar todos los campos!
          </div>
            <div v-if="correcto" class="alert alert-success" role="alert">
              Estamos trabajando en tu alerta! Si tu propiedad baja de precio recibiras un Whatsapp 😎
            </div>
        </div>
      </div>
    </div>

    </form>

    <!-- <div><button class="btn btn-primary" @click="getAllData" >
      get_barrios by this.axios </button>
                          </div> -->
                          



  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: "formulario-persona",
  data() {
    return {
      procesando: false,
      correcto: false,
      error: false,
      persona: {
        nombre: "",
        apellido: "",
        email: "",
        precioalerta: "",
        link: "",
        numero: ""
      },
    }
    },
   


    methods: {
        enviarFormulario() {
          this.procesando = true
          axios.post("http://127.0.0.1:4000/buscando ", this.persona)
          .then(data=>{
            console.log(data)
          })
          this.resetEstado();

        // Comprobamos la presencia de errores
        if (this.nombreInvalido || this.apellidoInvalido || this.emailInvalido || this.numeroInvalido || this.linkInvalido || this.numeroInvalido) {
          this.error = true;
        return;
        }

      this.$emit('add-persona', this.persona);
      this.$refs.nombre.focus()

        this.error = false;
        this.correcto = true;
        this.procesando = false;
        },
        // get_barrioss() {
        //   axios.get("http://127.0.0.1:4000/barrios ")
        //   .then(console.log(Response))
        // },
        // get_barrios() {
        //     this.axios
        //       .get('http://127.0.0.1:4000/barrios')
        //       .then(console.log(Response))
        //       // .then((res) => (this.msg = res.data))
        //   },da
      //   getAllData() {
      // try {
      //   const res =  axios.get("http://127.0.0.1:4000/barrios");

      //     const result = {
      //       status: res.status + "-" + res.statusText,
      //       headers: res.headers,
      //       data: res.data,
      //     };

      //     this.getResult = this.fortmatResponse(result);
      //   } catch (err) {
      //     this.getResult = this.fortmatResponse(err.response?.data) || err;
      //   }
      // },
        resetEstado(){
          this.correcto = false;
          this.error = false;
          this.procesando = true;
        },
    },
    computed: {
        nombreInvalido() {
      return this.persona.nombre.length < 1;
      },
      apellidoInvalido() {
      return this.persona.apellido.length < 1;
      },
      emailInvalido() {
      return this.persona.email.length < 1;
      },
      numeroInvalido() {
      return this.persona.numero.length < 1;
      },
      linkInvalido() {
      return this.persona.link.length < 1;
      },

    },
 }
 
</script>

<style scoped>
form {
  margin-bottom: 2rem;
}
</style>



