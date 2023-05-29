<article class="entry">
  <header class="entry-header">
    <h1 class="entry-title">{{ chart_title }}</h1>
    {% if virtual_table_nombre %}
    <h2 class="entry-subtitle">{{ virtual_table_nombre }}</h2>
    {% endif %}
  </header>

  <div class="entry-content">
  <div class="iframe-container">
    <iframe style="width:100%;max-width:100%;height:100vh" src="{{ superset_chart_url }}&standalone=true" class="alignfull" loading="lazy" frameborder="0" allowfullscreen></iframe>
  </div>

  <div class="entry-info">
    <div class="entry-description">
      {% if descripcion %}
      <h3>📝 Descripción</h3>
        <p>{{ descripcion }}</p>
      {% else %}
        <p>Gráfico basado en datos del Departamento de Córdoba."</p>
      {% endif %}
    </div>

    <div class="entry-source">
      {% if fuente %}
      <h3>🌐 Fuente</h3>
        <p><a href="{{ fuente }}">{{ url }}</a></p>
      {% endif %}
      </div>

      <div class="entry-analysis">
      {% if ia_analysis %}
      <h3>🔍 Análisis</h3>
        <p>{{ ia_analysis }}</p>
      
        {% endif %}
      </div>

    <div class="entry-description2">
      {% if virtual_table_descripcion %}
      <h3>ℹ️ Descripción Adicional</h3>
        <p>{{ virtual_table_descripcion }}</p>
     
      </div>
      {% endif %}
  </div>
</div>


  <div class="additional-info">
    <h2>ℹ️ Información Adicional</h2>
    <ul>
  {% if idic %}
    <li><strong>Código:</strong> {{ idic }}</li>
  {% endif %}
  
  {% if metodologia %}
    <li><strong>Metodología:</strong> {{ metodologia }}</li>
  {% endif %}
  
  {% if linea_base %}
    <li><strong>Línea Base:</strong> {{ linea_base }}</li>
  {% endif %}
  
  {% if source %}
    <li><strong>Fuente (Título):</strong> {{ fuente }}</li>
  {% endif %}
  
  {% if url %}
    <li><strong>Fuente (URL):</strong> <a href="{{ url }}">{{ url }}</a></li>
  {% endif %}
  
  {% if periodicidad %}
    <li><strong>Periodicidad:</strong> {{ periodicidad }}</li>
  {% endif %}
  
  {% if entidad_responsable %}
    <li><strong>Entidad Responsable:</strong> {{ entidad_responsable }}</li>
  {% endif %}
  
  {% if estrellas %}
    <li><strong>Estrellas:</strong> {{ estrellas }}</li>
  {% endif %}
  
  {% if superset_dataset_id %}
    <li class="metadata_to_hide"><strong>Superset Dataset ID:</strong> {{ superset_dataset_id }}</li>
  {% endif %}
  
  {% if virtual_data_source_id %}
    <li class="metadata_to_hide"><strong>Virtual Data Source ID:</strong> {{ virtual_data_source_id }}</li>
  {% endif %}
  
  {% if groupby %}
    <li class="metadata_to_hide"><strong>Groupby:</strong> {{ groupby }}</li>
  {% endif %}
  
  {% if x_axis_label %}
    <li class="metadata_to_hide"><strong>X Axis Label:</strong> {{ x_axis_label }}</li>
  {% endif %}
  
  {% if y_axis_label %}
    <li class="metadata_to_hide"><strong>Y Axis Label:</strong> {{ y_axis_label }}</li>
  {% endif %}
  
  {% if id %}
    <li class="metadata_to_hide"><strong>ID:</strong> {{ id }}</li>
  {% endif %}
  
  {% if metrics %}
    <li class="metadata_to_hide"><strong>Metrics:</strong> {{ metrics }}</li>
  {% endif %}
</ul>
  </div>
</article>

<style>
  :root {
    --primary-color: #528fee;
    --secondary-color: #123456;
    /* Agrega aquí más variables de color si es necesario */
  }

  body {
    background-color: var(--primary-color);
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }

  .entry {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    animation: fadeIn 0.5s ease;
  }

  .entry-header {
    flex-basis: 100%;
  }

  .entry-title {
    color: var(--secondary-color);
    margin: 0;
  }

  .entry-subtitle {
    margin: 5px 0;
    font-weight: normal;
  }

  .entry-content {
    display: flex;
    flex-basis: 100%;
    gap: 20px;
  }

  .iframe-container {
    flex-basis: 70%;
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
    overflow: hidden;
    max-width: 100%;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .entry-info {
    flex-basis: 30%;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .entry-info > div {
    flex-basis: 100%;
  }

  .entry-info h3 {
    margin: 0;
  }

  .entry-description2 {
    flex-basis: 100%;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
  }

  .additional-info {
    flex-basis: 100%;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
  }

  .additional-info h2 {
    margin: 0 0 10px;
  }

  .additional-info ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .additional-info ul li {
    margin-bottom: 5px;
  }

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>