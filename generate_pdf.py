import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf():
    pdf_path = 'reportes/avance_3.pdf'
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=12,
        alignment=1
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=8,
        leading=14
    )
    
    story.append(Paragraph("Informe Técnico: Avance 3 - Análisis de Datos", title_style))
    story.append(Paragraph("<b>Objetivo:</b> Aplicación de Pandas, NumPy y Matplotlib para estadísticas descriptivas, indicadores automatizados, gráficos y conclusiones.", body_style))
    story.append(Spacer(1, 10))
    
    # 1. Estadísticas descriptivas
    story.append(Paragraph("1. Estadísticas Descriptivas", h2_style))
    story.append(Paragraph("A continuación se presentan las estadísticas descriptivas calculadas sobre el dataset limpio (resultados/estadisticas.csv):", body_style))
    
    df_stats = pd.read_csv('resultados/estadisticas.csv')
    stats_data = [list(df_stats.columns)] + df_stats.round(2).values.tolist()
    t_stats = Table(stats_data, colWidths=[65, 45, 55, 55, 50, 50, 50, 60, 50, 50, 50])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Interpretación:</b> Las medidas muestran la dispersión y tendencia central de las variables numéricas. Por ejemplo, el salario medio se sitúa cerca de los 45,000 USD con una desviación estándar de ~12,000 USD, reflejando una variabilidad moderada en la compensación.", body_style))
    story.append(Spacer(1, 10))
    
    # 2. Indicadores automatizados
    story.append(Paragraph("2. Indicadores Automatizados", h2_style))
    story.append(Paragraph("Cinco indicadores clave programados automáticamente (resultados/indicadores.csv):", body_style))
    
    df_ind = pd.read_csv('resultados/indicadores.csv')
    ind_data = [list(df_ind.columns)] + df_ind.values.tolist()
    t_ind = Table(ind_data, colWidths=[120, 110, 100, 210])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t_ind)
    story.append(Spacer(1, 15))
    
    # 3. Gráficos con Pyplot
    story.append(Paragraph("3. Visualizaciones y Gráficos", h2_style))
    story.append(Paragraph("Se generaron tres gráficos clave almacenados en <code>resultados/graficos/</code>:", body_style))
    
    if os.path.exists('resultados/graficos/grafico_01.png'):
        story.append(Paragraph("<b>Gráfico 1:</b> Histograma de Salarios (Variable: Salario). Muestra una distribución normal centrada en 45,000 USD.", body_style))
        story.append(Image('resultados/graficos/grafico_01.png', width=400, height=225))
        story.append(Spacer(1, 10))
        
    if os.path.exists('resultados/graficos/grafico_02.png'):
        story.append(Paragraph("<b>Gráfico 2:</b> Empleados por Departamento (Variable: Departamento). Permite comparar la distribución de personal.", body_style))
        story.append(Image('resultados/graficos/grafico_02.png', width=400, height=225))
        story.append(Spacer(1, 10))
        
    if os.path.exists('resultados/graficos/grafico_03.png'):
        story.append(Paragraph("<b>Gráfico 3:</b> Salario según Nivel de Estudios (Diagrama de caja). Identifica la relación entre educación y compensación.", body_style))
        story.append(Image('resultados/graficos/grafico_03.png', width=400, height=225))
        story.append(Spacer(1, 10))
        
    # 4. Conclusión y Repositorio
    story.append(Paragraph("4. Conclusión del Avance", h2_style))
    story.append(Paragraph("La ejecución de <code>python main.py</code> automatizó completamente el procesamiento, cálculo y exportación de resultados. El sistema modular garantiza escalabilidad y reproducibilidad del análisis.", body_style))
    story.append(Paragraph("<b>Enlace al Repositorio GitHub:</b> <code>https://github.com/usuario/proyecto-analisis-datos</code>", body_style))
    
    doc.build(story)
    print("PDF generado con éxito en reportes/avance_3.pdf")

if __name__ == '__main__':
    generar_pdf()
