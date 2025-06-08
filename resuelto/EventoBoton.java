package bdmysql;

import java.awt.event.*;
import javax.swing.*;

public class EventoBoton implements ActionListener {
    private Ventana ventana;

    public EventoBoton(Ventana v) {
        this.ventana = v;
    }

    public void actionPerformed(ActionEvent e) {
        JButton boton = (JButton) e.getSource();
        String texto = boton.getText();

        switch (texto) {
            case "Primero": ventana.IrPrimero(); break;
            case "Anterior": ventana.IrAnterior(); break;
            case "Siguiente": ventana.IrSiguiente(); break;
            case "Ultimo": ventana.IrUltimo(); break;
            case "Insertar": ventana.IrInsertar(); ventana.IrActualizar(); break;
            case "Eliminar": ventana.IrEliminar(); ventana.IrActualizar(); break;
            case "Modificar": ventana.IrModificar(); ventana.IrActualizar(); break;
            case "Actualizar": ventana.IrActualizar(); break;
        }
    }
}
