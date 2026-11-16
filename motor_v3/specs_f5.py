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
