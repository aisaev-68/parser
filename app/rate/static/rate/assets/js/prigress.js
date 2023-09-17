var mix = {
  methods: {
    checkPaymentStatus() {
//      this.getData('/api/payment/')
//        .then(data => {
//          this.status = data.status;
          //alert("STATUS");
         // alert(this.status);
         setTimeout(() => {
               location.replace('/account/');
            }, 15000); // Переход через 30 секунд
  },
  mounted() {
    this.checkPaymentStatus();
  }
};