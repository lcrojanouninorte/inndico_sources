<article class="entry">
  <header class="entry-header">
    <h2 class="entry-title">{{ titulo_grafico }}</h2>
  </header>

  <div class="entry-content">
    <div class="iframe-container">
      <iframe src="{{ url_grafico }}" frameborder="0" allowfullscreen></iframe>
    </div>

    <div class="entry-description">
      <p>{{ descripcion }}</p>
    </div>

    <div class="entry-source">
      <p>Fuente: {{ fuente }}</p>
    </div>
  </div>
</article>

<style>
  .iframe-container {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%; /* Ajustar este valor para mantener la relación de aspecto del iframe */
    overflow: hidden;
    max-width: 100%;
  }

  .iframe-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
</style>