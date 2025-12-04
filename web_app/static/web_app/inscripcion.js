document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("inscripcionForm");
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Limpiar errores previos
        document.querySelectorAll('.error-message').forEach(el => el.innerHTML = '');
        document.querySelectorAll('.invalid').forEach(el => el.classList.remove('invalid'));

        try {
            const formData = {
                tutor_nombre: form.tutor_nombre.value,
                tutor_apellido: form.tutor_apellido.value,
                tutor_email: form.tutor_email.value,
                tutor_telefono: form.tutor_telefono.value,

                ninio_nombre: form.ninio_nombre.value,
                ninio_apellido: form.ninio_apellido.value,
                ninio_edad: form.ninio_edad.value,

                comentario: form.comentario.value,
            };

            fetch("/api/inscripcion/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {

                    if (!data.success) {
                        for (let campo in data.errors) {
                            const errorDiv = document.getElementById(`error_${campo}`);
                            if (errorDiv) {
                                errorDiv.innerHTML = data.errors[campo].join("<br>");
                                const input = form.querySelector(`[name$="${campo}"]`);
                                if (form[campo]) {
                                    form[campo].classList.add('invalid');
                                }
                            }
                        }
                        return;
                    }

                    // Mostrar modal de éxito
                    successModal.show();
                    form.reset();
                })
                .catch(err => {
                    console.error(err);
                    alert("Ocurrió un error inesperado. Por favor intentá nuevamente.");
                });
        } catch (error) {
            console.error("Error al procesar el formulario:", error);
            alert(`Error en el formulario: ${error.message}`);
        }
    });

});
