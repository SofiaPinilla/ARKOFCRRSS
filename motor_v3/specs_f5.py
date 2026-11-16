# -*- coding: utf-8 -*-
# Guiones y jugadas de los vídeos de FÚTBOL 5 (f5_01-f5_14). Motor v3, sport='f5' (campo de césped de F5).
# Formación: portero + rombo (y1 portero, y2 cierre, y3/y4 alas, y5 pívot). Rival r1..r5 en espejo.
# y=0 es la portería rival (arriba); tu equipo ataca hacia arriba.
import json, sys
from specs_fs import S, run, mv, drib, pas, shot, cut, ghost, tag, bub, zone, goal

CTA_VOICE = "¿Quieres jugar a fútbol 5 en Castellón? Únete a nuestro grupo de WhatsApp: enlace en la bio o escríbenos por DM."

V = {}

V['f5_01_rombo'] = dict(
  hook=["¿PRIMERA PACHANGA", "DE FÚTBOL 5?", "COLOCAOS EN ROMBO"],
  hook_voice="¿Primera pachanga de fútbol 5? Colocaos así: en rombo.",
  scenes=[
    S("1 · EL ROMBO", ["UNO ATRÁS, DOS ABIERTOS", "Y UNO ARRIBA"],
      "Uno: un cierre atrás, dos alas abiertas a las bandas y un pívot arriba.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[tag('y2', 'CIERRE', 0.08), tag('y3', 'ALA', 0.3), tag('y4', 'ALA', 0.45), tag('y5', 'PÍVOT', 0.62)]),
    S("2 · NUNCA EN LÍNEA", ["NUNCA DOS EN LA MISMA LÍNEA", "ASÍ SIEMPRE HAY PASE"],
      "Dos: nunca dos en la misma línea. Así siempre hay pase.",
      ball='y2', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.56]},
      ev=[ghost('y2', 'y5', 0.05, [0.5, 0.56]), pas('y2', 'y3', 0.35, 0.18), pas('y3', 'y5', 0.62, 0.2)]),
    S("3 · NO SE ROMPE", ["SI UNO SUBE, OTRO BAJA", "EL ROMBO NO SE ROMPE"],
      "Tres: si uno sube, otro ocupa su sitio. El rombo no se rompe.",
      ball='y2', focus=('y3', 'TÚ'),
      ev=[drib('y2', [0.5, 0.52], 0.08, 0.3), zone([0.5, 0.78], 'HUECO', 0.2, 0.3, 0.09), run('y3', [0.5, 0.76], 0.45, 0.3),
          tag('y3', 'CUBRE', 0.78)]),
  ])

V['f5_02_ala'] = dict(
  hook=["¿TE TOCA DE ALA?", "3 ERRORES QUE REGALAN GOLES", "¡EVÍTALOS!"],
  hook_voice="¿Te toca de ala en fútbol 5? Tres errores que regalan goles. ¡Evítalos!",
  scenes=[
    S("1 · NO VOLVER", ["¿LA PIERDES ARRIBA?", "CORRE ATRÁS"],
      "Uno: atacar pegado a la línea y no volver. Si la pierdes, corre atrás.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y4': [0.90, 0.26], 'r3': [0.72, 0.30]},
      ev=[cut('y4', 'y5', [0.72, 0.30], 0.05, 0.16), drib('r3', [0.78, 0.58], 0.3, 0.3, 'rrun'),
          zone([0.84, 0.66], 'HUECO', 0.3, 0.3, 0.09), run('y4', [0.86, 0.62], 0.5, 0.35)]),
    S("2 · CABEZA ARRIBA", ["CONDUCE CON LA CABEZA", "ARRIBA: EL PÍVOT ESTÁ SOLO"],
      "Dos: conducir sin levantar la cabeza. El pívot está solo.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y5': [0.42, 0.22], 'r2': [0.6, 0.30]},
      ev=[drib('y4', [0.80, 0.40], 0.05, 0.3), tag('y5', 'SOLO', 0.3), bub('y5', '¡AQUÍ!', 0.35, 0.3), pas('y4', 'y5', 0.62, 0.2)]),
    S("3 · SEGUNDO PALO", ["NO CHUTES SIEMPRE", "PASE AL SEGUNDO PALO"],
      "Tres: chutar siempre. El pase al segundo palo es gol seguro.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y4': [0.84, 0.20], 'y3': [0.30, 0.22], 'r2': [0.62, 0.14]},
      ev=[ghost('y4', [0.5, -0.02], 0.04, [0.62, 0.10]), run('y3', [0.38, 0.07], 0.25, 0.25), pas('y4', 'y3', 0.5, 0.18),
          shot('y3', 0.7, 0.45), goal(0.8)]),
  ])

CA = {'y2': [0.5, 0.52], 'y3': [0.2, 0.48], 'y4': [0.8, 0.48], 'y5': [0.5, 0.80], 'r2': [0.40, 0.24], 'r3': [0.62, 0.26], 'r4': [0.82, 0.72], 'r5': [0.5, 0.70]}
CL = {'y3': [0.18, 0.46], 'y2': [0.46, 0.64], 'y4': [0.84, 0.40], 'r3': [0.20, 0.37], 'r2': [0.32, 0.33], 'r4': [0.36, 0.45], 'r5': [0.28, 0.55]}

V['f5_03_dos_contra_uno'] = dict(
  hook=["TE VIENEN DOS", "Y ESTÁS SOLO ATRÁS", "¡HAZ ESTO!"],
  hook_voice="Te vienen dos y estás solo atrás. ¡Haz esto!",
  scenes=[
    S("1 · NO VAYAS", ["NO VAYAS A POR EL BALÓN", "RETROCEDE Y GANA TIEMPO"],
      "Uno: no vayas a por el balón. Retrocede y gana tiempo.",
      ball='r5', focus=('y2', 'TÚ'),
      pos={'y2': [0.5, 0.70], 'r5': [0.38, 0.50], 'r4': [0.72, 0.48], 'y3': [0.2, 0.30], 'y4': [0.8, 0.28], 'y5': [0.5, 0.22]},
      ev=[ghost('y2', [0.40, 0.55], 0.05, [0.44, 0.62]), run('y2', [0.5, 0.80], 0.35, 0.35), drib('r5', [0.40, 0.62], 0.35, 0.35, 'rrun'),
          run('r4', [0.72, 0.60], 0.35, 0.35, 'rrun')]),
    S("2 · EN MEDIO", ["PONTE EN MEDIO", "TAPA EL PASE ENTRE LOS DOS"],
      "Dos: ponte en medio, tapando el pase entre los dos.",
      ball='r5', focus=('y2', 'TÚ'),
      pos={'y2': [0.5, 0.80], 'r5': [0.40, 0.62], 'r4': [0.72, 0.60], 'y3': [0.2, 0.30], 'y4': [0.8, 0.28], 'y5': [0.5, 0.22]},
      ev=[run('y2', [0.56, 0.72], 0.08, 0.3), tag('y2', 'TAPA', 0.3), cut('r5', 'r4', [0.56, 0.71], 0.5, 0.15), bub('y2', '¡MÍA!', 0.72, 0.25)]),
    S("3 · QUE CHUTEN LEJOS", ["QUE CHUTEN DE LEJOS", "TU PORTERO HACE EL RESTO"],
      "Tres: que chuten de lejos. Tu portero hace el resto.",
      ball='r5', focus=('y2', 'TÚ'),
      pos={'y2': [0.56, 0.76], 'r5': [0.40, 0.64], 'r4': [0.72, 0.64], 'y3': [0.2, 0.30], 'y4': [0.8, 0.28], 'y5': [0.5, 0.22]},
      ev=[zone([0.42, 0.86], 'LEJOS', 0.05, 0.3, 0.08, 'lime'), pas('r5', 'y1', 0.4, 0.16), tag('y1', '¡PARADA!', 0.62)]),
  ])

V['f5_04_pivot'] = dict(
  hook=["¿TE TOCA DE PÍVOT?", "ASÍ TE LA PASAN SIEMPRE", "¡HAZ ESTO!"],
  hook_voice="¿Te toca de pívot? Así te la pasan siempre. ¡Haz esto!",
  scenes=[
    S("1 · MUÉVETE", ["MUÉVETE DE LADO A LADO", "QUIETO, TE TAPAN"],
      "Uno: muévete de lado a lado. Si te quedas quieto, te tapan.",
      ball='y2', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.30], 'r2': [0.5, 0.23], 'r5': [0.5, 0.52]},
      ev=[ghost('y2', 'y5', 0.05, [0.5, 0.52]), run('y5', [0.76, 0.32], 0.3, 0.25), mv('r2', [0.64, 0.25], 0.36, 0.3),
          pas('y2', 'y5', 0.66, 0.2)]),
    S("2 · AL PIE", ["PÍDELA AL PIE", "CON EL CUERPO DELANTE"],
      "Dos: pídela al pie, con el cuerpo entre el rival y el balón.",
      ball='y3', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.30], 'r2': [0.5, 0.23]},
      ev=[bub('y5', '¡AL PIE!', 0.05, 0.3), pas('y3', 'y5', 0.4, 0.2), tag('r2', 'DETRÁS', 0.7)]),
    S("3 · DESCARGA", ["¿NO TE GIRAS? DESCARGA", "Y ENTRA AL ÁREA"],
      "Tres: ¿no te puedes girar? Descarga y entra al área.",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.30], 'r2': [0.5, 0.23], 'y4': [0.76, 0.42]},
      ev=[pas('y5', 'y4', 0.06, 0.15), run('y5', [0.42, 0.12], 0.26, 0.25), pas('y4', 'y5', 0.56, 0.18), shot('y5', 0.78, 0.45), goal(0.88)]),
  ])

V['f5_05_paralela'] = dict(
  hook=["LA JUGADA MÁS FÁCIL", "DEL FÚTBOL 5", "LA PARALELA"],
  hook_voice="La jugada más fácil del fútbol 5: la paralela.",
  scenes=[
    S("1 · AL PÍVOT", ["EL ALA SE LA DA AL PÍVOT", "QUE ESTÁ DE ESPALDAS"],
      "Uno: el ala se la da al pívot, que está de espaldas.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y4': [0.86, 0.50], 'y5': [0.66, 0.32], 'r4': [0.80, 0.42], 'r2': [0.66, 0.25]},
      ev=[pas('y4', 'y5', 0.3, 0.2), tag('y5', 'DE ESPALDAS', 0.6)]),
    S("2 · SIGUE", ["EL ALA SIGUE CORRIENDO", "POR LA BANDA"],
      "Dos: el ala sigue corriendo por la banda.",
      ball='y5', focus=('y4', 'TÚ'), pos={'y4': [0.86, 0.50], 'y5': [0.66, 0.32], 'r4': [0.80, 0.42], 'r2': [0.66, 0.25]},
      ev=[run('y4', [0.92, 0.20], 0.08, 0.45), tag('r4', 'SE QUEDA', 0.65)]),
    S("3 · A LA ESPALDA", ["SE LA DEVUELVE A LA ESPALDA", "DEL DEFENSA. ¡GOL!"],
      "Tres: el pívot se la devuelve a la espalda del defensa. Gol.",
      ball='y5', focus=('y4', 'TÚ'), pos={'y4': [0.92, 0.22], 'y5': [0.66, 0.32], 'r4': [0.80, 0.42], 'r2': [0.66, 0.25]},
      ev=[pas('y5', 'y4', 0.08, 0.2), drib('y4', [0.78, 0.10], 0.33, 0.2), shot('y4', 0.58, 0.42), goal(0.72)]),
  ])

V['f5_06_cierre'] = dict(
  hook=["¿TE TOCA DE CIERRE?", "EL ERROR QUE REGALA GOLES", "¡OJO!"],
  hook_voice="¿Te toca de cierre? El error que regala goles. ¡Ojo!",
  scenes=[
    S("1 · EL ERROR", ["SUBES Y TE QUEDAS ARRIBA", "NADIE TE CUBRE"],
      "Uno: subir con el balón y quedarte arriba. Nadie te cubre.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[drib('y2', [0.5, 0.42], 0.05, 0.35), zone([0.5, 0.78], 'VACÍO', 0.45, 0.5, 0.1)]),
    S("2 · AVISA", ["SI SUBES, AVISA", "Y QUE BAJE UN ALA"],
      "Dos: si subes, avisa: ¡cúbreme!, y que baje un ala.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[drib('y2', [0.5, 0.50], 0.05, 0.3), bub('y2', '¡CÚBREME!', 0.15, 0.3), run('y3', [0.46, 0.76], 0.4, 0.35), tag('y3', 'CUBRE', 0.8)]),
    S("3 · DETRÁS DEL BALÓN", ["SIN BALÓN, SIEMPRE", "POR DETRÁS DEL BALÓN"],
      "Tres: sin balón, siempre por detrás de la línea del balón.",
      ball='r3', focus=('y2', 'TÚ'), pos={'r3': [0.22, 0.58], 'y2': [0.44, 0.48], 'y3': [0.24, 0.70]},
      ev=[zone([0.44, 0.48], 'MAL', 0.05, 0.2, 0.07), run('y2', [0.44, 0.74], 0.25, 0.35), tag('y2', 'BIEN', 0.72)]),
  ])

V['f5_07_marcar'] = dict(
  hook=["TU PAR NO TE LA METE", "SI HACES ESTO", "3 PASOS"],
  hook_voice="Tu par no te la mete si haces esto. Tres pasos.",
  scenes=[
    S("1 · QUE NO RECIBA", ["PONTE ENTRE ÉL", "Y EL BALÓN"],
      "Uno: que no reciba. Ponte entre él y el balón.",
      ball='r3', focus=('y2', 'TÚ'), pos={'r3': [0.20, 0.44], 'r5': [0.5, 0.66], 'y2': [0.5, 0.76], 'y3': [0.22, 0.52]},
      ev=[run('y2', [0.42, 0.62], 0.08, 0.3), cut('r3', 'r5', [0.42, 0.61], 0.5, 0.18), bub('y2', '¡MÍA!', 0.74, 0.22)]),
    S("2 · QUE NO SE GIRE", ["SI RECIBE, PÉGATE", "A SU ESPALDA"],
      "Dos: si recibe, que no se gire. Pégate a su espalda.",
      ball='r3', focus=('y2', 'TÚ'), pos={'r3': [0.20, 0.44], 'r5': [0.5, 0.64], 'y2': [0.5, 0.76], 'y3': [0.22, 0.52]},
      ev=[pas('r3', 'r5', 0.05, 0.2), run('y2', [0.5, 0.70], 0.28, 0.15), tag('r5', 'NO SE GIRA', 0.55)]),
    S("3 · A LA BANDA", ["SI SE GIRA, LLÉVALO", "A LA BANDA"],
      "Tres: si se gira, llévalo a la banda, lejos de la portería.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.64], 'y2': [0.45, 0.71], 'y3': [0.22, 0.52]},
      ev=[drib('r5', [0.82, 0.76], 0.12, 0.5, 'rrun'), run('y2', [0.76, 0.81], 0.14, 0.5), tag('r5', 'SIN ÁNGULO', 0.78)]),
  ])

V['f5_08_portero'] = dict(
  hook=["¿TE TOCA DE PORTERO", "EN FÚTBOL 5?", "JUEGA CON LOS PIES"],
  hook_voice="¿Te toca de portero en fútbol 5? Juega con los pies.",
  scenes=[
    S("1 · EL QUINTO", ["ERES EL QUINTO JUGADOR", "OFRÉCETE SI APRIETAN"],
      "Uno: eres el quinto jugador. Ofrécete cuando os aprieten.",
      ball='y2', focus=('y1', 'TÚ'), pos={'y2': [0.5, 0.78], 'r5': [0.5, 0.70], 'y4': [0.84, 0.66]},
      ev=[bub('y1', '¡ATRÁS!', 0.08, 0.3), pas('y2', 'y1', 0.35, 0.15), pas('y1', 'y4', 0.64, 0.2)]),
    S("2 · SAQUE RÁPIDO", ["SACA RÁPIDO Y AL LIBRE", "ANTES DE QUE SE COLOQUEN"],
      "Dos: saca rápido y al libre, antes de que se coloquen.",
      ball='y1', focus=('y1', 'TÚ'), pos={'y3': [0.14, 0.50]},
      ev=[tag('y3', 'LIBRE', 0.08), pas('y1', 'y3', 0.3, 0.22), drib('y3', [0.18, 0.30], 0.6, 0.3)]),
    S("3 · DE PIE", ["EN EL UNO CONTRA UNO", "AGUANTA DE PIE"],
      "Tres: en el uno contra uno, aguanta de pie hasta el final.",
      ball='r5', focus=('y1', 'TÚ'), pos={'r5': [0.5, 0.66], 'y2': [0.2, 0.70]},
      ev=[drib('r5', [0.5, 0.82], 0.05, 0.35, 'rrun'), mv('y1', [0.5, 0.90], 0.1, 0.3), pas('r5', 'y1', 0.5, 0.12), tag('y1', '¡PARADA!', 0.66)]),
  ])

V['f5_09_presion'] = dict(
  hook=["¿PRESIONAR ARRIBA", "EN FÚTBOL 5?", "ASÍ SÍ"],
  hook_voice="¿Presionar arriba en fútbol 5? Así sí.",
  scenes=[
    S("1 · SALE UNO", ["SALE UNO SOLO", "AL QUE TIENE EL BALÓN"],
      "Uno: sale uno solo, al que tiene el balón.",
      ball='r2', focus=('y5', 'TÚ'),
      ev=[run('y5', [0.5, 0.29], 0.1, 0.3), bub('y5', '¡VOY!', 0.12, 0.25)]),
    S("2 · AL MÁS CERCANO", ["LOS DEMÁS, CADA UNO", "A SU RIVAL MÁS CERCANO"],
      "Dos: los demás, cada uno al rival más cercano.",
      ball='r2', focus=('y3', 'TÚ'), pos={'y5': [0.5, 0.29]},
      ev=[run('y3', [0.22, 0.45], 0.06, 0.3), run('y4', [0.78, 0.45], 0.06, 0.3), run('y2', [0.5, 0.60], 0.2, 0.3),
          cut('r2', 'r3', [0.22, 0.44], 0.58, 0.15), tag('y3', 'ROBADA', 0.82)]),
    S("3 · TODOS ATRÁS", ["¿OS SUPERAN? TODOS ATRÁS", "CORRIENDO Y POR DENTRO"],
      "Tres: ¿os superan? Todos atrás corriendo, y por dentro.",
      ball='r3', focus=('y3', 'TÚ'), pos={'r3': [0.18, 0.50], 'y3': [0.24, 0.40], 'y4': [0.78, 0.42], 'y5': [0.5, 0.30]},
      ev=[drib('r3', [0.24, 0.62], 0.05, 0.3, 'rrun'), run('y3', [0.36, 0.70], 0.18, 0.4), run('y4', [0.62, 0.72], 0.18, 0.4),
          run('y5', [0.5, 0.58], 0.18, 0.4)]),
  ])

V['f5_10_reglas'] = dict(
  hook=["LAS REGLAS NO ESCRITAS", "DE LA PACHANGA", "¿LAS CUMPLES?"],
  hook_voice="Las reglas no escritas de la pachanga. ¿Las cumples?",
  scenes=[
    S("1 · LA PIERDES, VAS", ["EL QUE LA PIERDE", "VA A POR ELLA"],
      "Uno: el que la pierde, va a por ella.",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.22, 0.44], 'r3': [0.28, 0.38]},
      ev=[cut('y3', 'y5', [0.28, 0.38], 0.05, 0.12), drib('r3', [0.32, 0.58], 0.28, 0.3, 'rrun'), run('y3', [0.30, 0.54], 0.4, 0.3),
          bub('y3', '¡VOY!', 0.42, 0.25)]),
    S("2 · PÍDELA", ["SI ESTÁS SOLO,", "SE PIDE: «¡SOLO!»"],
      "Dos: si estás solo, se pide: ¡solo!",
      ball='y2', focus=('y4', 'TÚ'),
      ev=[bub('y4', '¡SOLO!', 0.12, 0.3), pas('y2', 'y4', 0.5, 0.2)]),
    S("3 · SIN ENTRADAS", ["NADA DE ENTRADAS FUERTES", "MAÑANA SE TRABAJA"],
      "Tres: nada de entradas fuertes. Mañana se trabaja.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.62], 'y2': [0.5, 0.75]},
      ev=[ghost('y2', 'r5', 0.05, [0.5, 0.685]), tag('y2', 'TRANQUI', 0.5), bub('r5', '¡GRACIAS!', 0.62, 0.3)]),
  ])

V['f5_11_contraataque'] = dict(
  hook=["CONTRAATAQUE 3 CONTRA 2", "¿QUÉ HACES?", "¡HAZ ESTO!"],
  hook_voice="Contraataque tres contra dos. ¿Qué haces? ¡Haz esto!",
  scenes=[
    S("1 · POR EL CENTRO", ["EL DEL BALÓN,", "POR EL CENTRO"],
      "Uno: el del balón, por el centro.",
      ball='y2', focus=('y2', 'TÚ'), pos=dict(CA),
      ev=[drib('y2', [0.5, 0.38], 0.1, 0.4)]),
    S("2 · ABIERTOS", ["LOS OTROS DOS, ABIERTOS", "Y POR DELANTE"],
      "Dos: los otros dos, abiertos y por delante.",
      ball='y2', focus=('y2', 'TÚ'), pos=dict(CA, y2=[0.5, 0.38]),
      ev=[run('y3', [0.14, 0.26], 0.08, 0.4), run('y4', [0.86, 0.26], 0.08, 0.4)]),
    S("3 · AL LIBRE", ["PÁSALA AL LADO", "AL QUE NO SALE EL DEFENSA"],
      "Tres: pásala al lado al que no sale el defensa. Gol.",
      ball='y2', focus=('y2', 'TÚ'), pos=dict(CA, y2=[0.5, 0.38], y3=[0.14, 0.26], y4=[0.86, 0.26]),
      ev=[mv('r3', [0.78, 0.27], 0.04, 0.2), tag('y3', 'LIBRE', 0.24), pas('y2', 'y3', 0.34, 0.18), shot('y3', 0.6, 0.35), goal(0.72)]),
  ])

V['f5_12_rota'] = dict(
  hook=["EN FÚTBOL 5", "NADIE TIENE SITIO FIJO", "¡ROTA!"],
  hook_voice="En fútbol 5 nadie tiene sitio fijo. ¡Rota!",
  scenes=[
    S("1 · EL PÍVOT BAJA", ["SI EL PÍVOT BAJA,", "UN ALA ENTRA ARRIBA"],
      "Uno: si el pívot baja a por el balón, un ala entra arriba.",
      ball='y2', focus=('y3', 'TÚ'),
      ev=[run('y5', [0.5, 0.50], 0.05, 0.3), pas('y2', 'y5', 0.3, 0.15), run('y3', [0.40, 0.26], 0.38, 0.35), tag('y3', 'PÍVOT', 0.78)]),
    S("2 · EL CIERRE ABRE", ["SI EL ALA SE METE DENTRO,", "EL CIERRE ABRE A LA BANDA"],
      "Dos: si el ala se mete por dentro, el cierre abre a la banda.",
      ball='y3', focus=('y2', 'TÚ'), pos={'y3': [0.18, 0.52]},
      ev=[run('y4', [0.62, 0.46], 0.05, 0.3), run('y2', [0.86, 0.58], 0.3, 0.32), tag('y2', 'ALA', 0.66), pas('y3', 'y2', 0.72, 0.2)]),
    S("3 · EL MÁS ATRÁS", ["AL PERDERLA, EL QUE ESTÁ", "MÁS ATRÁS HACE DE CIERRE"],
      "Tres: al perderla, el que está más atrás hace de cierre. Sin discutir.",
      ball='r5', focus=('y4', 'TÚ'), pos={'y2': [0.86, 0.42], 'y4': [0.62, 0.60], 'y3': [0.2, 0.42], 'y5': [0.5, 0.30], 'r5': [0.46, 0.52]},
      ev=[tag('y4', 'CIERRE', 0.12), run('y4', [0.5, 0.76], 0.2, 0.35), run('y2', [0.84, 0.62], 0.4, 0.3)]),
  ])

V['f5_13_queda_un_minuto'] = dict(
  hook=["VAS GANANDO", "Y QUEDA UN MINUTO", "¡CIÉRRALO!"],
  hook_voice="Vas ganando y queda un minuto. ¡Ciérralo!",
  scenes=[
    S("1 · AL PIE", ["BALÓN AL PIE", "NADA DE PELOTAZOS"],
      "Uno: balón al pie, nada de pelotazos.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[ghost('y2', [0.5, 0.06], 0.05, [0.5, 0.24]), pas('y2', 'y3', 0.4, 0.18), pas('y3', 'y2', 0.7, 0.18)]),
    S("2 · A LA ESQUINA", ["LLÉVALA A LA ESQUINA", "Y PROTÉGELA"],
      "Dos: llévala a la esquina contraria y protégela.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y4': [0.80, 0.36]},
      ev=[drib('y4', [0.93, 0.05], 0.08, 0.45), mv('r4', [0.86, 0.09], 0.15, 0.4), tag('y4', 'PROTEGE', 0.7)]),
    S("3 · TODOS DETRÁS", ["TODOS POR DETRÁS", "DEL BALÓN"],
      "Tres: todos por detrás del balón. Que nadie se quede arriba.",
      ball='r2', focus=('y5', 'TÚ'), pos={'r2': [0.5, 0.30], 'y5': [0.5, 0.18], 'y3': [0.2, 0.24], 'y4': [0.8, 0.22]},
      ev=[run('y5', [0.5, 0.46], 0.1, 0.4), run('y3', [0.24, 0.56], 0.1, 0.4), run('y4', [0.76, 0.56], 0.1, 0.4), tag('y5', 'ATRÁS', 0.7)]),
  ])

V['f5_14_cambia_de_lado'] = dict(
  hook=["¿TODOS VAN AL BALÓN?", "HAZ ESTO", "CAMBIA DE LADO"],
  hook_voice="¿Todos van al balón? Haz esto: cambia de lado.",
  scenes=[
    S("1 · EL OTRO LADO", ["SI SE AMONTONAN EN UN LADO", "EL OTRO ESTÁ LIBRE"],
      "Uno: si el rival se amontona en un lado, el otro está libre.",
      ball='y3', focus=('y4', 'TÚ'), pos=dict(CL),
      ev=[tag('r3', '¡TODOS!', 0.1), zone([0.78, 0.36], 'LIBRE', 0.3, 0.6, 0.11, 'lime')]),
    S("2 · AL ALA CONTRARIA", ["UN PASE AL ALA CONTRARIA", "Y ESTÁIS EN VENTAJA"],
      "Dos: un pase al ala contraria y ya estáis en ventaja.",
      ball='y3', focus=('y4', 'TÚ'), pos=dict(CL),
      ev=[pas('y3', 'y2', 0.06, 0.15), pas('y2', 'y4', 0.32, 0.22), drib('y4', [0.84, 0.18], 0.62, 0.3)]),
    S("3 · PÍDELO", ["PÍDELO EN VOZ ALTA:", "«¡CAMBIA!»"],
      "Tres: pídelo en voz alta: ¡cambia!",
      ball='y3', focus=('y4', 'TÚ'), pos=dict(CL),
      ev=[bub('y4', '¡CAMBIA!', 0.08, 0.35), pas('y3', 'y2', 0.4, 0.15), pas('y2', 'y4', 0.62, 0.22)]),
  ])

FK = {'y3': [0.5, 0.32], 'y5': [0.70, 0.30], 'y4': [0.82, 0.30], 'r2': [0.44, 0.20], 'r3': [0.52, 0.20], 'r4': [0.66, 0.16], 'r5': [0.30, 0.30]}

CK = {'y4': [0.97, 0.01], 'y5': [0.64, 0.12], 'y3': [0.42, 0.26], 'y2': [0.5, 0.55], 'r2': [0.58, 0.08], 'r3': [0.42, 0.15], 'r4': [0.68, 0.20], 'r5': [0.5, 0.42]}

V['f5_15_corner'] = dict(
  hook=["CÓRNER A FAVOR", "EN FÚTBOL 5", "COLOCAOS ASÍ"],
  hook_voice="Córner a favor en fútbol 5. Colocaos así.",
  scenes=[
    S("1 · PRIMER PALO", ["UNO AL PRIMER PALO", "PARA DESVIARLA"],
      "Uno: uno al primer palo, para desviarla.",
      ball='y4', focus=('y5', 'TÚ'), pos=dict(CK),
      ev=[run('y5', [0.60, 0.04], 0.08, 0.25), pas('y4', 'y5', 0.38, 0.18), shot('y5', 0.62, 0.46), goal(0.74)]),
    S("2 · LA FRONTAL", ["OTRO EN LA FRONTAL", "TIRO DE PRIMERAS"],
      "Dos: otro en la frontal, para chutar de primeras.",
      ball='y4', focus=('y3', 'TÚ'), pos=dict(CK),
      ev=[pas('y4', 'y3', 0.1, 0.22), shot('y3', 0.45, 0.42), goal(0.6)]),
    S("3 · UNO ATRÁS", ["SIEMPRE UNO ATRÁS", "VIGILANDO LA CONTRA"],
      "Tres: y siempre uno atrás, vigilando la contra.",
      ball='r2', focus=('y2', 'TÚ'), pos=dict(CK, y2=[0.62, 0.56]),
      ev=[tag('r5', 'SOLO ARRIBA', 0.05), run('y2', [0.52, 0.47], 0.28, 0.2), cut('r2', 'r5', [0.52, 0.46], 0.45, 0.2)]),
  ])

V['f5_16_falta'] = dict(
  hook=["FALTA AL BORDE", "DEL ÁREA", "NO CHUTES A LA BARRERA"],
  hook_voice="Falta al borde del área. No chutes a la barrera.",
  scenes=[
    S("1 · LA BARRERA", ["LA BARRERA TAPA", "EL TIRO DIRECTO"],
      "Uno: la barrera tapa el tiro directo.",
      ball='y3', focus=('y3', 'TÚ'), pos=dict(FK),
      ev=[tag('r3', 'BARRERA', 0.1), ghost('y3', [0.5, -0.02], 0.35, [0.5, 0.2])]),
    S("2 · A UN LADO", ["TOQUE CORTO A UN LADO", "Y CHUTA EL SEGUNDO"],
      "Dos: toque corto a un lado y chuta el segundo.",
      ball='y3', focus=('y5', 'TÚ'), pos=dict(FK),
      ev=[pas('y3', 'y5', 0.1, 0.15), shot('y5', 0.38, 0.38), goal(0.52)]),
    S("3 · POR DETRÁS", ["O ALGUIEN SE CUELA", "POR DETRÁS DE LA BARRERA"],
      "Tres: o alguien se cuela por detrás de la barrera.",
      ball='y3', focus=('y4', 'TÚ'), pos=dict(FK),
      ev=[run('y4', [0.64, 0.08], 0.08, 0.3), pas('y3', 'y4', 0.42, 0.18), shot('y4', 0.65, 0.45), goal(0.8)]),
  ])

V['f5_17_tapar_tiro'] = dict(
  hook=["EL RIVAL VA A CHUTAR", "¿DÓNDE TE PONES?", "¡AQUÍ!"],
  hook_voice="El rival va a chutar. ¿Dónde te pones? ¡Aquí!",
  scenes=[
    S("1 · EN LA LÍNEA", ["EN LA LÍNEA DEL TIRO", "TAPANDO EL PALO LARGO"],
      "Uno: ponte en la línea del tiro, tapando el palo largo.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.30, 0.66], 'y2': [0.56, 0.70]},
      ev=[ghost('r5', [0.56, 1.0], 0.05, None, 'shot'), run('y2', [0.40, 0.78], 0.3, 0.3), tag('y2', 'TAPAS', 0.7)]),
    S("2 · EL PORTERO, CORTO", ["TU PORTERO TAPA", "EL PALO CORTO"],
      "Dos: tu portero tapa el palo corto.",
      ball='r5', focus=('y1', 'PORTERO'), pos={'r5': [0.30, 0.66], 'y2': [0.40, 0.78]},
      ev=[mv('y1', [0.44, 0.93], 0.1, 0.3), tag('y1', 'CORTO', 0.5)]),
    S("3 · DE FRENTE", ["NO TE GIRES", "BLOQUEA DE FRENTE"],
      "Tres: no te gires ni cierres los ojos. Bloquea de frente.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.30, 0.66], 'y2': [0.40, 0.78], 'y1': [0.44, 0.93]},
      ev=[cut('r5', 'y1', [0.40, 0.77], 0.35, 0.12), tag('y2', '¡BLOQUEO!', 0.55)]),
  ])

V['f5_18_control'] = dict(
  hook=["¿TE LA PASAN", "Y LA PIERDES?", "CONTROLA ASÍ"],
  hook_voice="¿Te la pasan y la pierdes? Controla así.",
  scenes=[
    S("1 · MIRA ANTES", ["MIRA ANTES DE RECIBIR", "Y SABRÁS DÓNDE ESTÁ"],
      "Uno: mira antes de recibir. Así sabes dónde está el rival.",
      ball='y2', focus=('y3', 'TÚ'), pos={'y3': [0.20, 0.50], 'r3': [0.24, 0.42]},
      ev=[tag('r3', 'RIVAL', 0.12), pas('y2', 'y3', 0.5, 0.2)]),
    S("2 · ORIENTADO", ["CONTROLA HACIA DONDE", "NO ESTÁ EL RIVAL"],
      "Dos: controla hacia donde no está el rival.",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.20, 0.50], 'r3': [0.24, 0.42]},
      ev=[drib('y3', [0.38, 0.44], 0.1, 0.3), tag('r3', 'SUPERADO', 0.6)]),
    S("3 · DOS TOQUES", ["Y EN DOS TOQUES", "YA LA HAS SOLTADO"],
      "Tres: y en dos toques, ya la has soltado.",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.38, 0.44], 'r3': [0.24, 0.42]},
      ev=[pas('y3', 'y5', 0.25, 0.2), shot('y5', 0.6, 0.4), goal(0.75)]),
  ])

V['f5_19_te_encara'] = dict(
  hook=["¿TE ENCARA EL CRACK", "DEL OTRO EQUIPO?", "ASÍ LO PARAS"],
  hook_voice="¿Te encara el crack del otro equipo? Así lo paras.",
  scenes=[
    S("1 · NO TE TIRES", ["NO TE TIRES AL SUELO", "SI FALLAS, ES GOL"],
      "Uno: no te tires al suelo. Si fallas, es gol.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.60], 'y2': [0.5, 0.74]},
      ev=[tag('r5', 'CRACK', 0.05), ghost('y2', [0.5, 0.63], 0.3, [0.5, 0.67])]),
    S("2 · DE LADO", ["PONTE DE LADO", "Y LLÉVALO A LA BANDA"],
      "Dos: ponte de lado y llévalo a la banda.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.60], 'y2': [0.47, 0.72]},
      ev=[drib('r5', [0.80, 0.72], 0.1, 0.5, 'rrun'), run('y2', [0.74, 0.79], 0.12, 0.5)]),
    S("3 · DOBLA", ["PIDE AYUDA: «¡DOBLA!»", "DOS CONTRA UNO"],
      "Tres: pide ayuda: ¡dobla! Dos contra uno, se acabó.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.80, 0.72], 'y2': [0.74, 0.79], 'y4': [0.82, 0.54]},
      ev=[bub('y2', '¡DOBLA!', 0.05, 0.3), run('y4', [0.86, 0.66], 0.25, 0.3), tag('r5', 'ATRAPADO', 0.7)]),
  ])

V['f5_20_desmarque'] = dict(
  hook=["¿NO TE LLEGA", "NI UN BALÓN?", "DESMÁRCATE ASÍ"],
  hook_voice="¿No te llega ni un balón? Desmárcate así.",
  scenes=[
    S("1 · TAPADO", ["CON UN RIVAL DELANTE", "NO TE VEN"],
      "Uno: si tienes un rival delante, no te ven.",
      ball='y2', focus=('y4', 'TÚ'), pos={'y4': [0.72, 0.46], 'r4': [0.62, 0.55]},
      ev=[ghost('y2', 'y4', 0.2, [0.62, 0.55]), tag('r4', 'TE TAPA', 0.5)]),
    S("2 · ÁBRETE", ["MUÉVETE A UNA", "LÍNEA DE PASE LIMPIA"],
      "Dos: muévete a una línea de pase limpia.",
      ball='y2', focus=('y4', 'TÚ'), pos={'y4': [0.72, 0.46], 'r4': [0.62, 0.55]},
      ev=[run('y4', [0.88, 0.58], 0.08, 0.3), pas('y2', 'y4', 0.5, 0.2)]),
    S("3 · AL ESPACIO", ["Y SI PUEDES,", "PÍDELA AL ESPACIO"],
      "Tres: y si puedes, pídela al espacio, a la espalda del defensa.",
      ball='y2', focus=('y4', 'TÚ'), pos={'y4': [0.82, 0.46], 'r4': [0.80, 0.40]},
      ev=[run('y4', [0.88, 0.18], 0.08, 0.4), pas('y2', 'y4', 0.3, 0.25), tag('r4', 'SUPERADO', 0.75)]),
  ])

V['f5_21_pared'] = dict(
  hook=["EL TRUCO MÁS FÁCIL", "DEL FÚTBOL 5", "LA PARED"],
  hook_voice="El truco más fácil del fútbol 5: la pared.",
  scenes=[
    S("1 · PASA Y SIGUE", ["NO LE REGATEES", "PASA Y SIGUE CORRIENDO"],
      "Uno: no le regatees. Pasa y sigue corriendo.",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.30, 0.48], 'r3': [0.32, 0.38], 'y5': [0.52, 0.38]},
      ev=[pas('y3', 'y5', 0.12, 0.15), run('y3', [0.36, 0.24], 0.3, 0.35)]),
    S("2 · DE PRIMERAS", ["TE LA DEVUELVE", "DE PRIMERAS, A SU ESPALDA"],
      "Dos: te la devuelve de primeras, a su espalda.",
      ball='y5', focus=('y3', 'TÚ'), pos={'y3': [0.36, 0.26], 'r3': [0.32, 0.38], 'y5': [0.52, 0.38]},
      ev=[pas('y5', 'y3', 0.1, 0.18), drib('y3', [0.42, 0.12], 0.32, 0.2), shot('y3', 0.56, 0.4), goal(0.72)]),
    S("3 · PÍDELA", ["PÍDELA EN VOZ ALTA:", "«¡DAME Y VUELVE!»"],
      "Tres: pídela en voz alta: ¡dame y vuelve!",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.30, 0.48], 'r3': [0.32, 0.38], 'y5': [0.52, 0.38]},
      ev=[bub('y3', '¡DAME Y VUELVE!', 0.08, 0.35), pas('y3', 'y5', 0.5, 0.15)]),
  ])

V['f5_22_vas_perdiendo'] = dict(
  hook=["VAS PERDIENDO", "Y QUEDAN 5 MINUTOS", "¡NO TE VUELVAS LOCO!"],
  hook_voice="Vas perdiendo y quedan cinco minutos. ¡No te vuelvas loco!",
  scenes=[
    S("1 · NADA DE SOLOS", ["NO TE LA JUEGUES SOLO", "PASA Y MUÉVETE"],
      "Uno: no te la juegues solo. Pasa y muévete.",
      ball='y3', focus=('y3', 'TÚ'),
      ev=[ghost('y3', [0.26, 0.24], 0.05, [0.20, 0.40]), pas('y3', 'y5', 0.4, 0.2), run('y3', [0.30, 0.30], 0.55, 0.3)]),
    S("2 · CHUTA", ["SI HAY TIRO, CHUTA", "EL PORTERO TAMBIÉN FALLA"],
      "Dos: si hay tiro, chuta. El portero también falla.",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.30], 'r2': [0.62, 0.22]},
      ev=[tag('y5', 'TIRO', 0.1), shot('y5', 0.35, 0.42), goal(0.5)]),
    S("3 · RÁPIDO", ["TRAS EL GOL, BALÓN", "AL CENTRO, Y RÁPIDO"],
      "Tres: tras el gol, balón al centro y rápido. Cada segundo cuenta.",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.12]},
      ev=[drib('y5', [0.5, 0.49], 0.08, 0.45), tag('y5', '¡RÁPIDO!', 0.6)]),
  ])

V['f5_23_tipos'] = dict(
  hook=["EN TODA PACHANGA", "HAY UNO ASÍ", "¿CUÁL ERES TÚ?"],
  hook_voice="En toda pachanga hay uno así. ¿Cuál eres tú?",
  scenes=[
    S("1 · EL CHUPÓN", ["EL QUE NO LA SUELTA", "NI AUNQUE ESTÉS SOLO"],
      "Uno: el que no la suelta ni aunque estés solo.",
      ball='y3', focus=('y3', 'ÉL'), pos={'y5': [0.62, 0.30]},
      ev=[bub('y5', '¡SOLO!', 0.1, 0.35), drib('y3', [0.24, 0.42], 0.15, 0.4), tag('y3', 'CHUPÓN', 0.6)]),
    S("2 · EL TURISTA", ["EL QUE ATACA", "PERO NUNCA VUELVE"],
      "Dos: el que ataca, pero nunca vuelve.",
      ball='r5', focus=('y5', 'ÉL'), pos={'y5': [0.5, 0.18], 'r5': [0.5, 0.42]},
      ev=[drib('r5', [0.5, 0.80], 0.08, 0.5, 'rrun'), tag('y5', 'DE PASEO', 0.45)]),
    S("3 · EL DEL «¡HOMBRE!»", ["EL QUE GRITA «¡HOMBRE!»", "CUANDO YA ES TARDE"],
      "Tres: el que grita ¡hombre! cuando ya es tarde.",
      ball='y2', focus=('y4', 'ÉL'), pos={'r5': [0.34, 0.68]},
      ev=[cut('y2', 'y3', [0.34, 0.68], 0.1, 0.15), drib('r5', [0.30, 0.86], 0.35, 0.3, 'rrun'), bub('y4', '¡HOMBRE!', 0.6, 0.3)]),
  ])

for k, v in V.items():
    v['id'] = k
    v['sport'] = 'f5'
    v['cta_voice'] = CTA_VOICE

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/eng/specs_f5.json'
    json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
    takes = {k: [v['hook_voice']] + [s['voice'] for s in v['scenes']] + [v['cta_voice']] for k, v in V.items()}
    json.dump(takes, open(sys.argv[2] if len(sys.argv) > 2 else '/home/claude/eng/takes_f5.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in V.items():
        for s in v['scenes']:
            for l in s['sub']:
                if len(l) > 27: print('LONG', k, l, len(l))
    print(len(V), 'videos')
