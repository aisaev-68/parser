var mix = {
  methods: {
    UpdateStatus() {
      this.postData('/api/update/')
        .then(data => {
          this.status = data.message;  // Обновляем статус в соответствии с сообщением сервера
          // Перенаправляем пользователя на страницу с данными
          location.replace('/');
        })
        .catch(error => {
          console.error('Ошибка при обновлении данных:', error);
        });
    },
  },
  mounted() {
    this.UpdateStatus();
  }
};

