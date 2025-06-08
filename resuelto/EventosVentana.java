package bdmysql;

import java.awt.event.*;

public class EventosVentana extends WindowAdapter {
    private Ventana ventana;

    public EventosVentana(Ventana v) {
        this.ventana = v;
    }

    public void windowClosing(WindowEvent e) {
        System.exit(0);
    }
}
