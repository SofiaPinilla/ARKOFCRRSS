# -*- coding: utf-8 -*-
# Guiones y jugadas de los vídeos de FÚTBOL SALA (fs01-fs12). Mismo estilo que los de F7 (motor v3, sport='fs').
# Formación por defecto: portero + 1-2-1 (y1 portero, y2 cierre, y3/y4 alas, y5 pívot). Rival r1..r5 igual, en espejo.
import json, sys

CTA_VOICE = "¿Quieres jugar a fútbol sala sin tener equipo? Únete al grupo de WhatsApp. Enlace en la bio."

def S(title, sub, voice, ev=None, pos=None, ball=None, focus=None, hide=None):
    return dict(title=title, sub=sub, voice=voice, ev=ev or [], pos=pos or {}, ball=ball,
                focus=focus, hide=hide or [])

def run(p, to, t, d=0.3, a='run'):   return dict(k='mv', p=p, to=to, t=t, d=d, a=a)
def mv(p, to, t, d=0.3):             return dict(k='mv', p=p, to=to, t=t, d=d, a='none')
def drib(p, to, t, d=0.3, a='run'):  return dict(k='mv', p=p, to=to, t=t, d=d, a=a, drib=True)
def pas(fr, to, t, d=0.18):          return dict(k='pass', fr=fr, to=to, t=t, d=d, kind='pass')
def shot(fr, t, x=0.5, d=0.12):      return dict(k='pass', fr=fr, to=[x, -0.025], t=t, d=d, kind='shot')
def cut(fr, to, at, t, d=0.2):       return dict(k='pass', fr=fr, to=to, cut=at, t=t, d=d, kind='bad')
def ghost(fr, to, t, xat=None, kind='bad'): return dict(k='arrow', fr=fr, to=to, t=t, kind=kind, x=xat)
def tag(p, text, t):                 return dict(k='tag', p=p, text=text, t=t)
def bub(p, text, t, d=0.35):         return dict(k='bub', p=p, text=text, t=t, d=d)
def zone(at, text, t, d=1.0, r=0.085, col='red'): return dict(k='zone', at=at, text=text, t=t, d=d, r=r, col=col)
def goal(t):                         return dict(k='goal', t=t)

V = {}

V['fs01_pivot'] = dict(
  hook=["¿TE TOCA DE PÍVOT", "Y NO CONOCES A NADIE?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca de pívot y no conoces a nadie? ¡Haz esto!",
  scenes=[
    S("1 · DE ESPALDAS", ["JUEGA DE ESPALDAS", "PROTEGE CON EL CUERPO"],
      "Uno: juega de espaldas. Protege el balón con el cuerpo.",
      ball='y2', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.26], 'r2': [0.5, 0.20]},
      ev=[bub('y5', '¡DAME!', 0.05, 0.3), pas('y2', 'y5', 0.35, 0.22), tag('r2', 'DETRÁS', 0.65)]),
    S("2 · DEVUELVE", ["¿NO TE PUEDES GIRAR?", "DEVUÉLVELA Y VUELVE A PEDIR"],
      "Dos: si no te puedes girar, devuélvela y vuelve a pedirla.",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.5, 0.26], 'r2': [0.5, 0.20], 'y3': [0.22, 0.46]},
      ev=[ghost('y5', [0.5, 0.05], 0.04, [0.5, 0.17]), pas('y5', 'y3', 0.3, 0.16), run('y5', [0.62, 0.22], 0.45, 0.25),
          pas('y3', 'y5', 0.7, 0.18)]),
    S("3 · SEGUNDO PALO", ["CHUTA UN COMPAÑERO", "TÚ, AL SEGUNDO PALO"],
      "Tres: si chuta un compañero, tú al segundo palo.",
      ball='y3', focus=('y5', 'TÚ'), pos={'y3': [0.20, 0.24], 'y5': [0.5, 0.24], 'r2': [0.46, 0.17], 'r3': [0.24, 0.17]},
      ev=[run('y5', [0.60, 0.08], 0.08, 0.25), pas('y3', 'y5', 0.38, 0.2), shot('y5', 0.62, 0.56), goal(0.72)]),
  ])

V['fs02_cierre'] = dict(
  hook=["¿TE TOCA DE CIERRE", "CON DESCONOCIDOS?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca de cierre con desconocidos? ¡Haz esto!",
  scenes=[
    S("1 · ERES EL ÚLTIMO", ["ERES EL ÚLTIMO", "NO TE PASES DEL BALÓN"],
      "Uno: eres el último. Nunca te quedes por delante del balón.",
      ball='r5', focus=('y2', 'TÚ'), pos={'y2': [0.5, 0.48], 'r5': [0.46, 0.60], 'r3': [0.24, 0.70]},
      ev=[zone([0.5, 0.78], 'VACÍO', 0.04, 0.35, 0.1), run('y2', [0.44, 0.72], 0.3, 0.3)]),
    S("2 · ORDENA", ["TÚ LO VES TODO", "HABLA Y COLOCA A LOS TUYOS"],
      "Dos: tú lo ves todo. Habla y coloca a los tuyos.",
      ball='r3', focus=('y2', 'TÚ'), pos={'r3': [0.22, 0.48], 'r4': [0.80, 0.52], 'y4': [0.66, 0.40]},
      ev=[bub('y2', '¡CIERRA!', 0.06, 0.3), run('y4', [0.74, 0.56], 0.18, 0.3), bub('y2', '¡TUYO!', 0.5, 0.3),
          run('y3', [0.22, 0.56], 0.55, 0.25)]),
    S("3 · SALIDA SEGURA", ["CON BALÓN, NADA DE REGATES", "PASE SEGURO AL ALA"],
      "Tres: con balón, nada de regates. Pase seguro al ala.",
      ball='y2', focus=('y2', 'TÚ'), pos={'y2': [0.5, 0.74], 'r5': [0.5, 0.64]},
      ev=[ghost('y2', [0.5, 0.52], 0.05, [0.5, 0.64]), pas('y2', 'y4', 0.4, 0.2), tag('y4', 'SEGURO', 0.65)]),
  ])

V['fs03_ala'] = dict(
  hook=["¿TE TOCA DE ALA", "EN FÚTBOL SALA?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca de ala en fútbol sala? ¡Haz esto!",
  scenes=[
    S("1 · ÁBRETE", ["ÁBRETE PEGADO A LA BANDA", "ASÍ ABRES LA PISTA"],
      "Uno: ábrete pegado a la banda. Así abres la pista.",
      ball='y2', focus=('y4', 'TÚ'), pos={'y4': [0.70, 0.56], 'r4': [0.72, 0.46]},
      ev=[run('y4', [0.93, 0.54], 0.1, 0.3), run('r4', [0.86, 0.46], 0.2, 0.3, 'none'),
          zone([0.62, 0.38], 'HUECO', 0.5, 0.45, 0.09, 'lime')]),
    S("2 · LA PARALELA", ["PASA Y SIGUE POR LA BANDA", "LA PARALELA"],
      "Dos: pasa al pívot y sigue por la banda. La paralela.",
      ball='y4', focus=('y4', 'TÚ'), pos={'y4': [0.90, 0.54], 'y5': [0.62, 0.30], 'r4': [0.84, 0.46]},
      ev=[pas('y4', 'y5', 0.06, 0.18), run('y4', [0.92, 0.20], 0.25, 0.35), pas('y5', 'y4', 0.62, 0.18), tag('r4', 'SUPERADO', 0.8)]),
    S("3 · VUELVE", ["¿LA PIERDES? VUELVE", "AQUÍ DEFIENDEN LOS CINCO"],
      "Tres: ¿la pierdes? Vuelve. En fútbol sala defienden los cinco.",
      ball='r4', focus=('y4', 'TÚ'), pos={'y4': [0.90, 0.22], 'r4': [0.84, 0.40], 'r5': [0.62, 0.62]},
      ev=[run('y4', [0.84, 0.62], 0.1, 0.4), drib('r4', [0.82, 0.54], 0.3, 0.3, 'rrun'),
          cut('r4', 'r5', [0.78, 0.60], 0.66, 0.1)]),
  ])

V['fs04_portero'] = dict(
  hook=["¿TE TOCA PORTERÍA", "EN FÚTBOL SALA?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca portería en fútbol sala? ¡Haz esto!",
  scenes=[
    S("1 · HABLA", ["TÚ LO VES TODO", "HABLA SIN PARAR"],
      "Uno: tú lo ves todo. Habla sin parar.",
      ball='r4', focus=('y1', 'PORTERO'), pos={'r4': [0.80, 0.55]},
      ev=[bub('y1', '¡HOMBRE!', 0.08, 0.28), bub('y1', '¡SOLO!', 0.38, 0.26), bub('y1', '¡CIERRA!', 0.66, 0.3),
          run('y2', [0.6, 0.72], 0.72, 0.2, 'none')]),
    S("2 · SACA RÁPIDO", ["SAQUE CON LA MANO, AL LIBRE", "TIENES 4 SEGUNDOS"],
      "Dos: saca con la mano, rápido y al libre. Tienes cuatro segundos.",
      ball='y1', focus=('y1', 'PORTERO'), pos={'r5': [0.5, 0.70]},
      ev=[ghost('y1', [0.5, 0.40], 0.06, [0.5, 0.70]), tag('y3', 'LIBRE', 0.3), pas('y1', 'y3', 0.5, 0.2)]),
    S("3 · AGUANTA", ["EN EL UNO CONTRA UNO", "DE PIE Y HAZTE GRANDE"],
      "Tres: en el uno contra uno, aguanta de pie y hazte grande.",
      ball='r5', focus=('y1', 'PORTERO'), pos={'r5': [0.5, 0.66], 'y2': [0.62, 0.62]},
      ev=[drib('r5', [0.5, 0.82], 0.05, 0.35, 'rrun'), run('y1', [0.5, 0.88], 0.3, 0.15),
          cut('r5', [0.5, 1.0], [0.5, 0.88], 0.52, 0.08), tag('y1', '¡PARADA!', 0.62)]),
  ])

PW = {'y2': [0.42, 0.56], 'r5': [0.42, 0.46], 'y4': [0.70, 0.50], 'y5': [0.6, 0.28]}
V['fs05_pared'] = dict(
  hook=["EL TRUCO MÁS FÁCIL", "EN FÚTBOL SALA", "LA PARED"],
  hook_voice="El truco más fácil del fútbol sala: la pared.",
  scenes=[
    S("1 · PASA Y CORRE", ["NO LE REGATEES", "PASA Y SIGUE CORRIENDO"],
      "Uno: no le regatees. Pasa y sigue corriendo.",
      ball='y2', focus=('y2', 'TÚ'), pos=PW,
      ev=[ghost('y2', [0.42, 0.34], 0.05, [0.42, 0.46]), pas('y2', 'y4', 0.35, 0.16), run('y2', [0.48, 0.32], 0.5, 0.35)]),
    S("2 · DE PRIMERAS", ["TE LA DEVUELVE DE PRIMERAS", "A SU ESPALDA"],
      "Dos: te la devuelve de primeras, a su espalda.",
      ball='y4', focus=('y2', 'TÚ'), pos=dict(PW, y2=[0.44, 0.44], r5=[0.42, 0.50]),
      ev=[run('y2', [0.48, 0.30], 0.05, 0.35), pas('y4', 'y2', 0.25, 0.18), tag('r5', 'SUPERADO', 0.6)]),
    S("3 · PÍDELA", ["PÍDELA EN VOZ ALTA", "«¡DAME Y VUELVE!»"],
      "Tres: pídela en voz alta: ¡dame y vuelve!",
      ball='y2', focus=('y2', 'TÚ'), pos=PW,
      ev=[bub('y2', '¡DAME Y VUELVE!', 0.04, 0.3), pas('y2', 'y4', 0.3, 0.12), run('y2', [0.47, 0.24], 0.32, 0.25),
          pas('y4', 'y2', 0.48, 0.14), shot('y2', 0.68, 0.46), goal(0.78)]),
  ])

V['fs06_presion'] = dict(
  hook=["¿HAS PERDIDO EL BALÓN?", "TIENES 3 SEGUNDOS", "¡HAZ ESTO!"],
  hook_voice="¿Has perdido el balón? Tienes tres segundos. ¡Haz esto!",
  scenes=[
    S("1 · EL MÁS CERCANO", ["EL MÁS CERCANO", "A POR ÉL AL MOMENTO"],
      "Uno: el más cercano, a por él al momento.",
      ball='r3', focus=('y3', 'TÚ'), pos={'r3': [0.26, 0.44], 'y3': [0.20, 0.36]},
      ev=[run('y3', [0.27, 0.40], 0.1, 0.2), bub('y3', '¡VOY!', 0.35, 0.45)]),
    S("2 · TAPA PASES", ["LOS DEMÁS, NO AL BALÓN", "TAPAD AL MÁS CERCANO"],
      "Dos: los demás, no al balón. Tapad al rival más cercano.",
      ball='r3', pos={'r3': [0.26, 0.44], 'y3': [0.27, 0.40], 'r5': [0.5, 0.58], 'r2': [0.52, 0.30]},
      ev=[run('y2', [0.44, 0.56], 0.08, 0.25), run('y5', [0.47, 0.34], 0.16, 0.25), run('y4', [0.70, 0.46], 0.24, 0.25),
          ghost('r3', 'r5', 0.62, [0.44, 0.56])]),
    S("3 · TODOS ATRÁS", ["¿NO LA ROBAS?", "TODOS ATRÁS, POR DENTRO"],
      "Tres: ¿no la robas? Todos atrás y por dentro.",
      ball='r3', pos={'r3': [0.26, 0.40], 'y3': [0.30, 0.38]},
      ev=[bub('y1', '¡ATRÁS!', 0.04, 0.3), run('y2', [0.5, 0.78], 0.15, 0.3), run('y3', [0.34, 0.64], 0.15, 0.3),
          run('y4', [0.64, 0.66], 0.2, 0.3), run('y5', [0.5, 0.56], 0.2, 0.3)]),
  ])

V['fs07_te_encara'] = dict(
  hook=["¿TE ENCARA EL CRACK", "DEL OTRO EQUIPO?", "¡ASÍ LO PARAS!"],
  hook_voice="¿Te encara el crack del otro equipo? ¡Así lo paras!",
  scenes=[
    S("1 · NI AL SUELO", ["NO TE TIRES AL SUELO", "SI FALLAS, ES GOL"],
      "Uno: no te tires al suelo. Si fallas, es gol.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.58], 'y2': [0.5, 0.72]},
      ev=[ghost('y2', [0.40, 0.60], 0.06, [0.40, 0.60]), drib('r5', [0.62, 0.84], 0.4, 0.3, 'rrun')]),
    S("2 · A LA BANDA", ["PONTE DE LADO", "Y LLÉVALO A LA BANDA"],
      "Dos: ponte de lado y llévalo a la banda.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.5, 0.58], 'y2': [0.5, 0.72], 'y4': [0.80, 0.80]},
      ev=[mv('y2', [0.44, 0.68], 0.08, 0.2), drib('r5', [0.80, 0.66], 0.32, 0.4, 'rrun'),
          run('y2', [0.72, 0.72], 0.36, 0.4)]),
    S("3 · PIDE AYUDA", ["PIDE AYUDA: ¡DOBLA!", "DOS CONTRA UNO, SE ACABÓ"],
      "Tres: pide ayuda. ¡Dobla! Dos contra uno, se acabó.",
      ball='r5', focus=('y2', 'TÚ'), pos={'r5': [0.80, 0.64], 'y2': [0.70, 0.72], 'y4': [0.86, 0.84]},
      ev=[bub('y2', '¡DOBLA!', 0.05, 0.35), run('y4', [0.90, 0.58], 0.25, 0.3),
          cut('r5', [0.97, 0.48], [0.90, 0.58], 0.62, 0.1)]),
  ])

V['fs08_nadie_te_la_pasa'] = dict(
  hook=["¿NADIE TE LA PASA", "EN LA PACHANGA?", "¡HAZ ESTO!"],
  hook_voice="¿Nadie te la pasa en la pachanga de fútbol sala? ¡Haz esto!",
  scenes=[
    S("1 · DESMÁRCATE", ["TAPADO NO TE VEN", "BUSCA UNA LÍNEA LIMPIA"],
      "Uno: tapado no te ven. Busca una línea de pase limpia.",
      ball='y2', focus=('y4', 'TÚ'), pos={'y4': [0.66, 0.44], 'r4': [0.62, 0.52]},
      ev=[ghost('y2', 'y4', 0.06, [0.62, 0.52]), run('y4', [0.84, 0.56], 0.3, 0.3), pas('y2', 'y4', 0.68, 0.22)]),
    S("2 · PÍDELA", ["PÍDELA CON VOZ Y MANO", "QUE TE OIGAN: ¡SOLO!"],
      "Dos: pídela con la voz y con la mano. ¡Solo!",
      ball='y2', focus=('y4', 'TÚ'),
      ev=[bub('y4', '¡SOLO!', 0.08, 0.55), pas('y2', 'y4', 0.6, 0.2)]),
    S("3 · FÁCIL Y BIEN", ["LAS PRIMERAS, FÁCIL", "Y TE LA PASARÁN SIEMPRE"],
      "Tres: las primeras, fácil. Y te la pasarán siempre.",
      ball='y2', focus=('y4', 'TÚ'),
      ev=[pas('y2', 'y4', 0.08, 0.15), pas('y4', 'y2', 0.3, 0.15), pas('y2', 'y4', 0.55, 0.15), bub('y2', '¡TOMA!', 0.5, 0.3)]),
  ])

TWO = ['y1', 'y2', 'y3', 'r3', 'r4', 'r5']
V['fs09_dos_contra_uno'] = dict(
  hook=["2 CONTRA 1", "¿QUÉ HACES?", "¡ASÍ NO FALLAS!"],
  hook_voice="Dos contra uno en fútbol sala. ¿Qué haces? ¡Así no fallas!",
  scenes=[
    S("1 · CONDUCE", ["CONDUCE HACIA EL DEFENSA", "NO TE ABRAS A LA BANDA"],
      "Uno: conduce hacia el defensa, no te abras a la banda.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.40, 0.58], 'y4': [0.70, 0.50], 'r2': [0.5, 0.26]},
      ev=[ghost('y5', [0.08, 0.38], 0.05, [0.18, 0.46]), drib('y5', [0.45, 0.40], 0.38, 0.35)]),
    S("2 · SI SALE, PASA", ["SI SALE A POR TI", "PASE AL COMPAÑERO SOLO"],
      "Dos: si sale a por ti, pase al compañero, que se queda solo.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.45, 0.40], 'y4': [0.70, 0.34], 'r2': [0.5, 0.24]},
      ev=[mv('r2', [0.47, 0.33], 0.06, 0.25), pas('y5', 'y4', 0.36, 0.15), drib('y4', [0.64, 0.16], 0.52, 0.15, 'none'),
          shot('y4', 0.68, 0.53), goal(0.78)]),
    S("3 · SI NO, CHUTA", ["SI SE QUEDA CON ÉL", "SIGUE TÚ Y CHUTA"],
      "Tres: si se queda con él, sigue tú y chuta.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.45, 0.40], 'y4': [0.70, 0.34], 'r2': [0.5, 0.24]},
      ev=[mv('r2', [0.64, 0.29], 0.06, 0.25), drib('y5', [0.45, 0.16], 0.32, 0.25), shot('y5', 0.64, 0.46), goal(0.74)]),
  ])

SB = {'y3': [0.0, 0.42], 'y5': [0.26, 0.30], 'y2': [0.30, 0.54], 'r3': [0.18, 0.50], 'r5': [0.40, 0.46], 'r2': [0.34, 0.26]}
V['fs10_saque_de_banda'] = dict(
  hook=["EN FÚTBOL SALA", "LA BANDA SE SACA CON EL PIE", "¡APROVÉCHALO!"],
  hook_voice="En fútbol sala, la banda se saca con el pie. ¡Aprovéchalo!",
  scenes=[
    S("1 · SÁCALA RÁPIDO", ["BALÓN PARADO EN LA LÍNEA", "Y SÁCALA RÁPIDO"],
      "Uno: balón parado en la línea, y sácala rápido.",
      ball='y3', focus=('y3', 'TÚ'), pos=SB,
      ev=[pas('y3', 'y2', 0.12, 0.15), run('r3', [0.24, 0.56], 0.2, 0.5, 'none'), drib('y2', [0.36, 0.40], 0.4, 0.3)]),
    S("2 · 4 SEGUNDOS", ["TIENES 4 SEGUNDOS", "BUSCA AL LIBRE"],
      "Dos: tienes cuatro segundos. Busca al que está libre.",
      ball='y3', focus=('y3', 'TÚ'), pos=SB,
      ev=[bub('y5', '¡AQUÍ, AQUÍ!', 0.04, 0.4), ghost('y3', 'y5', 0.3, [0.30, 0.28]), tag('y2', 'LIBRE', 0.45), pas('y3', 'y2', 0.6, 0.18)]),
    S("3 · ENTRA RÁPIDO", ["DESPUÉS DE SACAR", "ENTRA RÁPIDO A LA PISTA"],
      "Tres: después de sacar, entra rápido a la pista.",
      ball='y3', focus=('y3', 'TÚ'), pos=SB,
      ev=[pas('y3', 'y2', 0.06, 0.15), run('y3', [0.14, 0.30], 0.28, 0.3), pas('y2', 'y3', 0.66, 0.15)]),
  ])

CF = {'y4': [0.985, 0.012], 'r1': [0.5, 0.03], 'r2': [0.46, 0.10], 'r3': [0.62, 0.11], 'r4': [0.40, 0.20], 'r5': [0.5, 0.42],
      'y5': [0.60, 0.17], 'y3': [0.42, 0.30], 'y2': [0.5, 0.58], 'y1': [0.5, 0.945]}
V['fs11_corner'] = dict(
  hook=["CÓRNER A FAVOR", "EN FÚTBOL SALA", "¡COLOCAOS ASÍ!"],
  hook_voice="Córner a favor en fútbol sala. ¡Colocaos así!",
  scenes=[
    S("1 · PRIMER PALO", ["UNO AL PRIMER PALO", "A RASO, PARA DESVIARLA"],
      "Uno: uno al primer palo. Pase raso para desviarla.",
      ball='y4', focus=('y5', 'TÚ'), pos=CF,
      ev=[run('y5', [0.60, 0.06], 0.08, 0.3), pas('y4', 'y5', 0.42, 0.16), shot('y5', 0.62, 0.45), goal(0.72)]),
    S("2 · LA FRONTAL", ["OTRO EN LA FRONTAL", "TIRO DE PRIMERAS"],
      "Dos: otro en la frontal, para chutar de primeras.",
      ball='y4', focus=('y3', 'TÚ'), pos=CF,
      ev=[pas('y4', 'y3', 0.1, 0.22), shot('y3', 0.45, 0.42), goal(0.58)]),
    S("3 · UNO ATRÁS", ["SIEMPRE UNO ATRÁS", "VIGILANDO LA CONTRA"],
      "Tres: y siempre uno atrás, vigilando la contra.",
      ball='r2', focus=('y2', 'TÚ'), pos=dict(CF, r5=[0.30, 0.46], y2=[0.56, 0.58]),
      ev=[tag('r5', 'SOLO ARRIBA', 0.05), run('y2', [0.38, 0.50], 0.3, 0.2), cut('r2', 'r5', [0.38, 0.50], 0.45, 0.2)]),
  ])

V['fs12_primeros_5_min'] = dict(
  hook=["¿PRIMERA PACHANGA", "DE FÚTBOL SALA?", "5 MINUTOS CLAVE"],
  hook_voice="¿Primera pachanga de fútbol sala sin conocer a nadie? Cinco minutos clave.",
  scenes=[
    S("1 · NADA DE INVENTOS", ["NADA DE INVENTOS", "TOQUES FÁCILES Y CERCA"],
      "Uno: nada de inventos. Toques fáciles y cerca.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[ghost('y2', [0.5, 0.20], 0.05, [0.5, 0.40]), pas('y2', 'y3', 0.38, 0.15), pas('y3', 'y2', 0.62, 0.15)]),
    S("2 · OBSERVA", ["MIRA QUIÉN ES RÁPIDO", "Y QUIÉN NO DEFIENDE"],
      "Dos: mira quién es rápido y quién no defiende.",
      ball='y2', focus=('y2', 'TÚ'),
      ev=[tag('y4', 'RÁPIDO', 0.12), tag('y3', 'ZURDO', 0.38), tag('y5', 'NO DEFIENDE', 0.62)]),
    S("3 · ROTA", ["¿CANSADO? PIDE EL CAMBIO", "AQUÍ SE ROTA SIN PARAR"],
      "Tres: ¿cansado? Pide el cambio. Aquí se rota sin parar.",
      ball='y2', focus=('y3', 'TÚ'), pos={'y3': [0.20, 0.54]},
      ev=[bub('y3', '¡CAMBIO!', 0.06, 0.35), run('y3', [0.02, 0.47], 0.3, 0.3), tag('y3', 'FUERA', 0.62)]),
  ])

for k, v in V.items():
    v['id'] = k
    v['sport'] = 'fs'
    v['cta_voice'] = CTA_VOICE

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/eng/specs_fs.json'
    json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
    takes = {k: [v['hook_voice']] + [s['voice'] for s in v['scenes']] + [v['cta_voice']] for k, v in V.items()}
    json.dump(takes, open('/home/claude/eng/takes_fs.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in V.items():
        for s in v['scenes']:
            for l in s['sub']:
                if len(l) > 27: print('LONG', k, l, len(l))
    print(len(V), 'videos')
