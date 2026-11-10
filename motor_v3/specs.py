# -*- coding: utf-8 -*-
# Guiones y jugadas de los vídeos 02-19 (estilo vídeo de referencia futbol7_v4)
import json

CTA_VOICE = "¿Quieres jugar F7 sin tener equipo? Únete al grupo de WhatsApp. Enlace en la bio."

def S(title, sub, voice, ev=None, pos=None, ball=None, focus=None, hide=None):
    return dict(title=title, sub=sub, voice=voice, ev=ev or [], pos=pos or {}, ball=ball,
                focus=focus, hide=hide or [])

# helpers for events
def run(p, to, t, d=0.3, a='run'):   return dict(k='mv', p=p, to=to, t=t, d=d, a=a)
def mv(p, to, t, d=0.3):             return dict(k='mv', p=p, to=to, t=t, d=d, a='none')
def drib(p, to, t, d=0.3, a='run'):  return dict(k='mv', p=p, to=to, t=t, d=d, a=a, drib=True)
def pas(fr, to, t, d=0.18):          return dict(k='pass', fr=fr, to=to, t=t, d=d, kind='pass')
def shot(fr, t, x=0.5, d=0.12):      return dict(k='pass', fr=fr, to=[x, -0.025], t=t, d=d, kind='shot')
def cut(fr, to, at, t, d=0.2):       return dict(k='pass', fr=fr, to=to, cut=at, t=t, d=d, kind='bad')
def ghost(fr, to, t, xat=None, kind='bad'): return dict(k='arrow', fr=fr, to=to, t=t, kind=kind, x=xat)
def tag(p, text, t):                 return dict(k='tag', p=p, text=text, t=t)
def bub(p, text, t, d=0.35):         return dict(k='bub', p=p, text=text, t=t, d=d)
def zone(at, text, t, d=1.0, r=0.075, col='red'): return dict(k='zone', at=at, text=text, t=t, d=d, r=r, col=col)
def goal(t):                         return dict(k='goal', t=t)

V = {}

V['02_delantero'] = dict(
  hook=["¿TE TOCA DELANTERO", "Y NO CONOCES A NADIE?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca delantero y no conoces a nadie? ¡Haz esto!",
  scenes=[
    S("1 · DESMÁRCATE", ["NO TE QUEDES QUIETO", "SAL A LA ESPALDA DEL DEFENSA"],
      "Uno: no te quedes quieto. Sal a la espalda del defensa.",
      ball='y5', focus=('y7', 'TÚ'), pos={'y7': [0.42, 0.30], 'r2': [0.48, 0.22]},
      ev=[run('y7', [0.62, 0.12], 0.12, 0.35), pas('y5', 'y7', 0.38, 0.25)]),
    S("2 · PRESIONA", ["SIN BALÓN, PRESIONA TÚ", "TÁPALE EL PASE AL MEDIO"],
      "Dos: sin balón, presiona tú. Tápale el pase al medio.",
      ball='r2', focus=('y7', 'TÚ'), pos={'y7': [0.62, 0.30]},
      ev=[run('y7', [0.43, 0.29], 0.1, 0.3), cut('r2', 'r5', [0.43, 0.29], 0.55)]),
    S("3 · ¡CHUTA!", ["SI TIENES TIRO, ¡CHUTA!", "EN PACHANGA, EL QUE TIRA MARCA"],
      "Tres: si tienes tiro, chuta. En pachanga, el que tira, marca.",
      ball='y7', focus=('y7', 'TÚ'), pos={'y7': [0.40, 0.30], 'r2': [0.58, 0.20]},
      ev=[drib('y7', [0.42, 0.20], 0.08, 0.25), shot('y7', 0.42, 0.44), goal(0.55)]),
  ])

V['03_lateral'] = dict(
  hook=["¿TE TOCA LATERAL", "CON DESCONOCIDOS?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca lateral con desconocidos? ¡Haz esto!",
  scenes=[
    S("1 · CIERRA", ["BALÓN EN LA OTRA BANDA", "CIERRA HACIA DENTRO"],
      "Uno: balón en la otra banda, cierra hacia dentro.",
      ball='r6', focus=('y3', 'TÚ'), pos={'r6': [0.86, 0.56], 'y4': [0.80, 0.64], 'r7': [0.42, 0.68]},
      ev=[zone([0.32, 0.76], 'HUECO', 0.05, 0.42), run('y3', [0.32, 0.75], 0.25, 0.3)]),
    S("2 · SUBE CON CABEZA", ["SUBE SOLO SI TE CUBREN", "AVISA: ¡CÚBREME!"],
      "Dos: sube solo si te cubren. Avisa: ¡cúbreme!",
      ball='y6', focus=('y3', 'TÚ'),
      ev=[bub('y3', '¡CÚBREME!', 0.05, 0.4), run('y3', [0.10, 0.36], 0.15, 0.4),
          run('y5', [0.20, 0.72], 0.35, 0.3), pas('y6', 'y3', 0.68, 0.22)]),
    S("3 · PASE ATRÁS", ["NO CHUTES DESDE LA BANDA", "PASE ATRÁS AL QUE LLEGA"],
      "Tres: no chutes desde la banda. Pase atrás al que llega.",
      ball='y3', focus=('y3', 'TÚ'), pos={'y3': [0.10, 0.11], 'y7': [0.56, 0.30], 'r2': [0.40, 0.14], 'r3': [0.22, 0.17]},
      ev=[ghost('y3', [0.40, 0.0], 0.05, [0.3, 0.05]), run('y7', [0.52, 0.17], 0.3, 0.2),
          pas('y3', 'y7', 0.45, 0.15), shot('y7', 0.66, 0.56), goal(0.76)]),
  ])

V['04_crack'] = dict(
  hook=["¿QUIÉN ES EL BUENO", "DE TU EQUIPO?", "¡DESCÚBRELO!"],
  hook_voice="¿Quién es el bueno de tu equipo? ¡Descúbrelo!",
  scenes=[
    S("1 · PIDE EL BALÓN", ["SIEMPRE PIDE EL BALÓN", "AUNQUE TENGA A UNO ENCIMA"],
      "Uno: siempre pide el balón, aunque tenga a uno encima.",
      ball='y5', focus=('y6', 'EL BUENO'), pos={'r6': [0.72, 0.50]},
      ev=[bub('y6', '¡DAME!', 0.08, 0.4), pas('y5', 'y6', 0.5, 0.2)]),
    S("2 · PRIMER CONTROL", ["LA PARA PEGADA AL PIE", "Y LEVANTA LA CABEZA"],
      "Dos: la para pegada al pie y levanta la cabeza.",
      ball='y2', focus=('y6', 'EL BUENO'),
      ev=[pas('y2', 'y6', 0.1, 0.22), drib('y6', [0.66, 0.46], 0.4, 0.22, a='none'),
          ghost('y6', 'y7', 0.66, None, 'look'), ghost('y6', 'y4', 0.72, None, 'look')]),
    S("3 · NO ABUSES", ["BÚSCALE, PERO NO SIEMPRE", "SI LE DOBLAN, HAY OTRO LIBRE"],
      "Tres: búscale, pero no siempre. Si le doblan, hay otro libre.",
      ball='y5', focus=('y6', 'EL BUENO'),
      ev=[run('r6', [0.74, 0.52], 0.05, 0.25, 'none'), run('r5', [0.60, 0.50], 0.1, 0.25, 'none'),
          ghost('y5', 'y6', 0.38, [0.6, 0.555]), tag('y7', 'LIBRE', 0.55), pas('y5', 'y7', 0.68, 0.2)]),
  ])

V['05_mediocentro'] = dict(
  hook=["¿TE TOCA EN EL MEDIO", "CON GENTE NUEVA?", "¡MANDA TÚ!"],
  hook_voice="¿Te toca en el medio con gente nueva? ¡Manda tú!",
  scenes=[
    S("1 · MIRA ANTES", ["ANTES DE RECIBIR", "MIRA POR ENCIMA DEL HOMBRO"],
      "Uno: antes de recibir, mira por encima del hombro.",
      ball='y2', focus=('y5', 'TÚ'),
      ev=[ghost('y5', 'y7', 0.08, None, 'look'), ghost('y5', 'y3', 0.2, None, 'look'),
          pas('y2', 'y5', 0.42, 0.2), pas('y5', 'y7', 0.72, 0.18)]),
    S("2 · RECIBE DE LADO", ["BUSCA EL HUECO", "Y RECIBE DE LADO"],
      "Dos: busca el hueco y recibe de lado.",
      ball='y2', focus=('y5', 'TÚ'), pos={'y5': [0.33, 0.38], 'r5': [0.34, 0.47], 'r6': [0.58, 0.46]},
      ev=[ghost('y2', 'y5', 0.06, [0.34, 0.47]), run('y5', [0.46, 0.55], 0.28, 0.3),
          pas('y2', 'y5', 0.64, 0.2)]),
    S("3 · CORTA EL PASE", ["SIN BALÓN, NO LA PERSIGAS", "CORTA LA LÍNEA DE PASE"],
      "Tres: sin balón, no la persigas. Corta la línea de pase.",
      ball='r5', focus=('y5', 'TÚ'), pos={'y5': [0.22, 0.52], 'r7': [0.48, 0.70]},
      ev=[run('y5', [0.40, 0.57], 0.12, 0.3), cut('r5', 'r7', [0.40, 0.57], 0.5)]),
  ])

V['06_portero'] = dict(
  hook=["¿TE TOCA PORTERÍA", "Y NO CONOCES A NADIE?", "¡HAZ ESTO!"],
  hook_voice="¿Te toca portería y no conoces a nadie? ¡Haz esto!",
  scenes=[
    S("1 · HABLA", ["TÚ LO VES TODO", "HABLA SIN PARAR"],
      "Uno: tú lo ves todo. Habla sin parar.",
      ball='r6', focus=('y1', 'PORTERO'), pos={'y2': [0.62, 0.80]},
      ev=[bub('y1', '¡HOMBRE!', 0.08, 0.28), bub('y1', '¡SOLO!', 0.38, 0.26), bub('y1', '¡SAL!', 0.66, 0.34),
          run('y2', [0.62, 0.70], 0.72, 0.2, 'none'), run('y3', [0.17, 0.66], 0.72, 0.2, 'none'), run('y4', [0.83, 0.66], 0.72, 0.2, 'none')]),
    S("2 · SACA CORTO", ["NADA DE PELOTAZOS", "SAQUE RÁPIDO Y CORTO"],
      "Dos: nada de pelotazos. Saque rápido y corto.",
      ball='y1', focus=('y1', 'PORTERO'),
      ev=[ghost('y1', [0.5, 0.30], 0.06, [0.5, 0.44]), pas('y1', 'y3', 0.45, 0.22)]),
    S("3 · DECIDE", ["EN EL UNO CONTRA UNO", "SAL CON TODO O QUÉDATE"],
      "Tres: en el uno contra uno, sal con todo o quédate.",
      ball='r7', focus=('y1', 'PORTERO'), pos={'r7': [0.5, 0.60], 'y2': [0.62, 0.58]},
      ev=[drib('r7', [0.5, 0.79], 0.05, 0.35, 'rrun'), run('y1', [0.5, 0.85], 0.32, 0.18),
          cut('r7', [0.5, 1.0], [0.5, 0.85], 0.52, 0.08), tag('y1', '¡PARADA!', 0.6)]),
  ])

V['07_pared'] = dict(
  hook=["EL TRUCO MÁS FÁCIL", "PARA SUPERAR A UN RIVAL", "LA PARED"],
  hook_voice="El truco más fácil para superar a un rival: la pared.",
  scenes=[
    S("1 · PASA Y CORRE", ["NO LE REGATEES", "PASA Y SIGUE CORRIENDO"],
      "Uno: no le regatees. Pasa y sigue corriendo.",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.40, 0.50], 'r5': [0.40, 0.41], 'y6': [0.64, 0.46], 'y7': [0.70, 0.31]},
      ev=[ghost('y5', [0.40, 0.30], 0.05, [0.40, 0.41]), pas('y5', 'y6', 0.35, 0.16), run('y5', [0.46, 0.27], 0.5, 0.35)]),
    S("2 · DE PRIMERAS", ["TE LA DEVUELVE DE PRIMERAS", "A SU ESPALDA"],
      "Dos: te la devuelve de primeras, a su espalda.",
      ball='y6', focus=('y5', 'TÚ'), pos={'y5': [0.42, 0.40], 'r5': [0.40, 0.45], 'y6': [0.64, 0.46], 'y7': [0.70, 0.31]},
      ev=[run('y5', [0.47, 0.25], 0.05, 0.35), pas('y6', 'y5', 0.25, 0.18), tag('r5', 'SUPERADO', 0.6)]),
    S("3 · PÍDELA", ["PÍDELA EN VOZ ALTA", "«¡DAME Y VUELVE!»"],
      "Tres: pídela en voz alta: ¡dame y vuelve!",
      ball='y5', focus=('y5', 'TÚ'), pos={'y5': [0.40, 0.50], 'r5': [0.40, 0.41], 'y6': [0.64, 0.46], 'y7': [0.70, 0.31]},
      ev=[bub('y5', '¡DAME Y VUELVE!', 0.04, 0.3), pas('y5', 'y6', 0.3, 0.12), run('y5', [0.46, 0.22], 0.32, 0.25),
          pas('y6', 'y5', 0.48, 0.14), shot('y5', 0.68, 0.48), goal(0.78)]),
  ])

V['08_presion'] = dict(
  hook=["¿HAS PERDIDO EL BALÓN?", "TIENES 5 SEGUNDOS", "¡HAZ ESTO!"],
  hook_voice="¿Has perdido el balón? Tienes cinco segundos. ¡Haz esto!",
  scenes=[
    S("1 · EL MÁS CERCANO", ["EL MÁS CERCANO", "PRESIONA AL MOMENTO"],
      "Uno: el más cercano presiona al momento.",
      ball='r5', focus=('y6', 'TÚ'), pos={'r5': [0.58, 0.50]},
      ev=[run('y6', [0.62, 0.525], 0.1, 0.2), bub('y6', '¡VOY!', 0.35, 0.45)]),
    S("2 · TAPA PASES", ["LOS DEMÁS, NO AL BALÓN", "TAPA AL RIVAL MÁS CERCANO"],
      "Dos: los demás, no al balón. Tapa al rival más cercano.",
      ball='r5', pos={'r5': [0.58, 0.50], 'y6': [0.62, 0.53], 'r7': [0.42, 0.66]},
      ev=[run('y5', [0.47, 0.60], 0.08, 0.25), run('y7', [0.5, 0.27], 0.16, 0.25), run('y4', [0.74, 0.47], 0.24, 0.25),
          ghost('r5', 'r7', 0.62, [0.47, 0.60])]),
    S("3 · TODOS JUNTOS", ["¿NO LA RECUPERAS?", "TODOS ATRÁS Y JUNTOS"],
      "Tres: ¿no la recuperas? Todos atrás y juntos.",
      ball='r5', pos={'r5': [0.58, 0.45], 'y6': [0.62, 0.50], 'y7': [0.5, 0.30]},
      ev=[bub('y2', '¡ATRÁS!', 0.04, 0.3), run('y5', [0.38, 0.65], 0.15, 0.3), run('y6', [0.62, 0.65], 0.15, 0.3),
          run('y7', [0.5, 0.55], 0.15, 0.3), run('y3', [0.26, 0.77], 0.2, 0.3), run('y4', [0.74, 0.77], 0.2, 0.3)]),
  ])

V['09_te_encara'] = dict(
  hook=["¿TE ENCARA EL CRACK", "DEL OTRO EQUIPO?", "¡ASÍ LO PARAS!"],
  hook_voice="¿Te encara el crack del otro equipo? ¡Así lo paras!",
  scenes=[
    S("1 · NI AL SUELO", ["NO TE TIRES AL SUELO", "NI ENTRES A LO LOCO"],
      "Uno: no te tires al suelo, ni entres a lo loco.",
      ball='r7', focus=('y2', 'TÚ'), pos={'r7': [0.5, 0.63], 'y2': [0.5, 0.77]},
      ev=[ghost('y2', [0.38, 0.65], 0.06, [0.38, 0.65]), drib('r7', [0.66, 0.84], 0.4, 0.3, 'rrun')]),
    S("2 · A LA BANDA", ["PONTE DE LADO", "Y LLÉVALO A LA BANDA"],
      "Dos: ponte de lado y llévalo a la banda.",
      ball='r7', focus=('y2', 'TÚ'), pos={'r7': [0.5, 0.63], 'y2': [0.5, 0.77], 'y4': [0.86, 0.90]},
      ev=[mv('y2', [0.44, 0.73], 0.08, 0.2), drib('r7', [0.80, 0.70], 0.32, 0.4, 'rrun'),
          run('y2', [0.70, 0.75], 0.36, 0.4)]),
    S("3 · PIDE AYUDA", ["PIDE AYUDA: ¡DOBLA!", "DOS CONTRA UNO, SE ACABÓ"],
      "Tres: pide ayuda. ¡Dobla! Dos contra uno, se acabó.",
      ball='r7', focus=('y2', 'TÚ'), pos={'r7': [0.78, 0.68], 'y2': [0.68, 0.76], 'y4': [0.86, 0.90]},
      ev=[bub('y2', '¡DOBLA!', 0.05, 0.35), run('y4', [0.90, 0.62], 0.25, 0.3),
          cut('r7', [0.97, 0.52], [0.90, 0.62], 0.62, 0.1)]),
  ])

V['10_nadie_te_la_pasa'] = dict(
  hook=["¿NADIE TE LA PASA", "EN LA PACHANGA?", "¡HAZ ESTO!"],
  hook_voice="¿Nadie te la pasa en la pachanga? ¡Haz esto!",
  scenes=[
    S("1 · DESMÁRCATE", ["TAPADO NO TE VEN", "BUSCA UNA LÍNEA LIMPIA"],
      "Uno: tapado no te ven. Busca una línea de pase limpia.",
      ball='y2', focus=('y6', 'TÚ'), pos={'y6': [0.70, 0.38], 'r6': [0.66, 0.47]},
      ev=[ghost('y2', 'y6', 0.06, [0.66, 0.47]), run('y6', [0.84, 0.50], 0.3, 0.3), pas('y2', 'y6', 0.68, 0.22)]),
    S("2 · PÍDELA", ["PÍDELA CON VOZ Y MANO", "QUE TE OIGAN: ¡SOLO!"],
      "Dos: pídela con la voz y con la mano. ¡Solo!",
      ball='y5', focus=('y6', 'TÚ'),
      ev=[bub('y6', '¡SOLO!', 0.08, 0.55), pas('y5', 'y6', 0.6, 0.2)]),
    S("3 · FÁCIL Y BIEN", ["LAS PRIMERAS, FÁCIL", "Y TE LA PASARÁN SIEMPRE"],
      "Tres: las primeras, fácil. Y te la pasarán siempre.",
      ball='y5', focus=('y6', 'TÚ'),
      ev=[pas('y5', 'y6', 0.08, 0.15), pas('y6', 'y5', 0.3, 0.15), pas('y5', 'y6', 0.55, 0.15), bub('y5', '¡TOMA!', 0.5, 0.3)]),
  ])

V['11_banda'] = dict(
  hook=["¿JUEGAS POR BANDA?", "3 CLAVES PARA ROMPERLA", "¡APUNTA!"],
  hook_voice="¿Juegas por banda? Tres claves para romperla. ¡Apunta!",
  scenes=[
    S("1 · ÁBRETE", ["ÁBRETE, PEGADO A LA LÍNEA", "Y ABRES HUECO DENTRO"],
      "Uno: ábrete, pegado a la línea, y abres hueco dentro.",
      ball='y5', focus=('y6', 'TÚ'), pos={'y6': [0.70, 0.42], 'r4': [0.74, 0.30]},
      ev=[run('y6', [0.93, 0.38], 0.1, 0.35), run('r4', [0.86, 0.32], 0.2, 0.35, 'none'),
          zone([0.62, 0.28], 'HUECO', 0.55, 0.45, 0.08, 'lime')]),
    S("2 · PASE ATRÁS", ["NO LA CUELGUES", "PASE RASO AL PENALTI"],
      "Dos: no la cuelgues. Pase raso al punto de penalti.",
      ball='y6', focus=('y6', 'TÚ'), pos={'y6': [0.90, 0.10], 'y7': [0.56, 0.30], 'r4': [0.80, 0.14]},
      ev=[ghost('y6', [0.5, 0.06], 0.05, [0.5, 0.07]), run('y7', [0.5, 0.16], 0.3, 0.2),
          pas('y6', 'y7', 0.45, 0.15), shot('y7', 0.66), goal(0.76)]),
    S("3 · VUELVE", ["SI LA PIERDES, VUELVE", "NO DEJES SOLO AL LATERAL"],
      "Tres: si la pierdes, vuelve. No dejes solo al lateral.",
      ball='r4', focus=('y6', 'TÚ'), pos={'y6': [0.90, 0.22], 'r4': [0.84, 0.40], 'r6': [0.66, 0.52], 'y4': [0.82, 0.70]},
      ev=[tag('y4', 'SOLO CONTRA 2', 0.02), run('y6', [0.88, 0.58], 0.12, 0.42),
          drib('r4', [0.83, 0.52], 0.3, 0.3, 'rrun'), cut('r4', 'r6', [0.86, 0.57], 0.66, 0.08)]),
  ])

TWO = ['y2', 'y3', 'y4', 'y6', 'r3', 'r4', 'r5', 'r6', 'r7']
V['12_dos_contra_uno'] = dict(
  hook=["2 CONTRA 1", "¿QUÉ HACES?", "¡ASÍ NO FALLAS!"],
  hook_voice="Dos contra uno. ¿Qué haces? ¡Así no fallas!",
  scenes=[
    S("1 · CONDUCE", ["CONDUCE HACIA EL DEFENSA", "NO TE ABRAS A LA BANDA"],
      "Uno: conduce hacia el defensa, no te abras a la banda.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.40, 0.58], 'y7': [0.68, 0.50], 'r2': [0.5, 0.26]},
      ev=[ghost('y5', [0.10, 0.36], 0.05, [0.2, 0.46]), drib('y5', [0.45, 0.40], 0.38, 0.35)]),
    S("2 · SI SALE, PASA", ["SI SALE A POR TI", "PASE AL COMPAÑERO SOLO"],
      "Dos: si sale a por ti, pase al compañero, que se queda solo.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.45, 0.40], 'y7': [0.68, 0.34], 'r2': [0.5, 0.24]},
      ev=[mv('r2', [0.47, 0.33], 0.06, 0.25), pas('y5', 'y7', 0.36, 0.15), drib('y7', [0.64, 0.18], 0.52, 0.15, 'none'),
          shot('y7', 0.68, 0.52), goal(0.78)]),
    S("3 · SI NO, CHUTA", ["SI SE QUEDA CON ÉL", "SIGUE TÚ Y CHUTA"],
      "Tres: si se queda con él, sigue tú y chuta.",
      ball='y5', focus=('y5', 'TÚ'), hide=TWO, pos={'y5': [0.45, 0.40], 'y7': [0.68, 0.34], 'r2': [0.5, 0.24]},
      ev=[mv('r2', [0.63, 0.29], 0.06, 0.25), drib('y5', [0.45, 0.18], 0.32, 0.25), shot('y5', 0.64, 0.46), goal(0.74)]),
  ])

V['13_primeros_5_min'] = dict(
  hook=["¿PRIMERA PACHANGA", "SIN CONOCER A NADIE?", "5 MINUTOS CLAVE"],
  hook_voice="¿Primera pachanga sin conocer a nadie? Cinco minutos clave.",
  scenes=[
    S("1 · NADA DE INVENTOS", ["NADA DE INVENTOS", "TOQUES FÁCILES Y CERCA"],
      "Uno: nada de inventos. Toques fáciles y cerca.",
      ball='y5', focus=('y5', 'TÚ'),
      ev=[ghost('y5', [0.36, 0.10], 0.05, [0.35, 0.30]), pas('y5', 'y6', 0.38, 0.15), pas('y6', 'y5', 0.62, 0.15)]),
    S("2 · OBSERVA", ["MIRA QUIÉN ES RÁPIDO", "Y QUIÉN NO DEFIENDE"],
      "Dos: mira quién es rápido y quién no defiende.",
      ball='y5', focus=('y5', 'TÚ'),
      ev=[tag('y4', 'RÁPIDO', 0.12), tag('y3', 'ZURDO', 0.38), tag('y7', 'NO DEFIENDE', 0.62)]),
    S("3 · TU ZONA", ["NO VAYÁIS TODOS AL BALÓN", "QUÉDATE EN TU ZONA"],
      "Tres: no vayáis todos al balón. Quédate en tu zona.",
      ball='r5', focus=('y5', 'TÚ'),
      pos={'r5': [0.5, 0.48], 'y5': [0.43, 0.52], 'y6': [0.57, 0.53], 'y7': [0.5, 0.42], 'y3': [0.40, 0.58], 'y4': [0.60, 0.59]},
      ev=[ghost('y3', 'r5', 0.03, [0.45, 0.53]), run('y5', [0.33, 0.56], 0.3, 0.3), run('y6', [0.67, 0.56], 0.3, 0.3),
          run('y3', [0.17, 0.76], 0.35, 0.3), run('y4', [0.83, 0.76], 0.35, 0.3), run('y7', [0.5, 0.30], 0.4, 0.3)]),
  ])

CF = {'y4': [0.985, 0.012], 'r1': [0.5, 0.03], 'r2': [0.45, 0.09], 'r3': [0.6, 0.085], 'r4': [0.70, 0.11],
      'r5': [0.38, 0.14], 'r6': [0.58, 0.15], 'r7': [0.5, 0.36], 'y7': [0.62, 0.17], 'y5': [0.42, 0.28],
      'y6': [0.72, 0.24], 'y3': [0.30, 0.20], 'y2': [0.5, 0.55]}
V['14_corner_a_favor'] = dict(
  hook=["CÓRNER A FAVOR", "SIN CONOCEROS", "¡COLOCAOS ASÍ!"],
  hook_voice="Córner a favor sin conoceros. ¡Colocaos así!",
  scenes=[
    S("1 · PRIMER PALO", ["UNO AL PRIMER PALO", "PARA PEINARLA"],
      "Uno: uno al primer palo, para peinarla.",
      ball='y4', focus=('y7', 'TÚ'), pos=CF,
      ev=[run('y7', [0.61, 0.06], 0.08, 0.3), pas('y4', 'y7', 0.42, 0.16), shot('y7', 0.62, 0.44), goal(0.72)]),
    S("2 · LA FRONTAL", ["OTRO EN LA FRONTAL", "A POR EL RECHACE"],
      "Dos: otro en la frontal, a por el rechace.",
      ball='y4', focus=('y5', 'TÚ'), pos=CF,
      ev=[pas('y4', [0.52, 0.08], 0.06, 0.16), pas([0.52, 0.08], 'y5', 0.3, 0.18), shot('y5', 0.6, 0.55), goal(0.7)]),
    S("3 · UNO ATRÁS", ["SIEMPRE UNO ATRÁS", "VIGILANDO LA CONTRA"],
      "Tres: siempre uno atrás, vigilando la contra.",
      ball='r2', focus=('y2', 'TÚ'), pos=dict(CF, r7=[0.30, 0.50], y2=[0.56, 0.60]),
      ev=[tag('r7', 'SOLO ARRIBA', 0.05), run('y2', [0.40, 0.53], 0.3, 0.2), cut('r2', 'r7', [0.40, 0.53], 0.45, 0.2)]),
  ])

CC = {'r3': [0.015, 0.988], 'y1': [0.5, 0.965], 'y2': [0.5, 0.90], 'y3': [0.33, 0.92], 'y4': [0.66, 0.91],
      'y5': [0.36, 0.80], 'y6': [0.62, 0.80], 'y7': [0.5, 0.62], 'r2': [0.42, 0.88], 'r5': [0.56, 0.86],
      'r6': [0.68, 0.94], 'r7': [0.40, 0.83], 'r4': [0.5, 0.72]}
V['15_corner_en_contra'] = dict(
  hook=["CÓRNER EN CONTRA", "SIN CONOCER A NADIE", "¡QUE NO TE PILLEN!"],
  hook_voice="Córner en contra sin conocer a nadie. ¡Que no te pillen!",
  scenes=[
    S("1 · CADA UNO, UNO", ["CADA UNO CON UN RIVAL", "PÉGATE AL QUE TENGAS CERCA"],
      "Uno: cada uno con un rival. Pégate al que tengas cerca.",
      ball='r3', focus=('y5', 'TÚ'), pos=CC,
      ev=[run('y5', [0.38, 0.855], 0.08, 0.25), run('y6', [0.58, 0.83], 0.18, 0.25), run('y2', [0.45, 0.92], 0.28, 0.2),
          run('y4', [0.66, 0.965], 0.36, 0.2), run('y7', [0.48, 0.75], 0.44, 0.2)]),
    S("2 · MANDA EL PORTERO", ["SI EL PORTERO GRITA ¡MÍA!", "TODOS FUERA"],
      "Dos: si el portero grita ¡mía!, todos fuera.",
      ball='r3', focus=('y1', 'PORTERO'),
      pos=dict(CC, y5=[0.38, 0.855], y6=[0.58, 0.83], y2=[0.45, 0.92], y4=[0.66, 0.965], y7=[0.48, 0.75]),
      ev=[bub('y1', '¡MÍA!', 0.06, 0.4), run('y1', [0.5, 0.92], 0.22, 0.25), pas('r3', 'y1', 0.22, 0.25),
          mv('y2', [0.40, 0.95], 0.2, 0.2)]),
    S("3 · SALID JUNTOS", ["AL DESPEJAR", "SALID TODOS JUNTOS"],
      "Tres: al despejar, salid todos juntos.",
      ball='y1', focus=('y2', 'TÚ'),
      pos=dict(CC, y1=[0.5, 0.92], y5=[0.38, 0.855], y6=[0.58, 0.83], y2=[0.45, 0.92], y4=[0.66, 0.965], y7=[0.48, 0.75]),
      ev=[pas('y1', [0.78, 0.42], 0.06, 0.22), run('y2', [0.45, 0.74], 0.3, 0.3), run('y3', [0.30, 0.74], 0.3, 0.3),
          run('y4', [0.66, 0.76], 0.3, 0.3), run('y5', [0.38, 0.64], 0.34, 0.3), run('y6', [0.6, 0.62], 0.34, 0.3)]),
  ])

HI = {'y5': [0.33, 0.30], 'y6': [0.67, 0.28], 'y7': [0.5, 0.17], 'y3': [0.14, 0.36], 'y4': [0.86, 0.36], 'y2': [0.5, 0.42]}
V['16_vas_perdiendo'] = dict(
  hook=["¿VAS PERDIENDO 3-0?", "NO OS VOLVÁIS LOCOS", "¡HACED ESTO!"],
  hook_voice="¿Vas perdiendo tres a cero? No os volváis locos. ¡Haced esto!",
  scenes=[
    S("1 · DOS ATRÁS", ["NO SUBÁIS LOS SIETE", "SIEMPRE DOS ATRÁS"],
      "Uno: no subáis los siete. Siempre dos atrás.",
      ball='y6', focus=('y2', 'TÚ'), pos=dict(HI, r7=[0.5, 0.58]),
      ev=[zone([0.5, 0.72], 'VACÍO', 0.03, 0.3, 0.1), run('y2', [0.42, 0.66], 0.32, 0.3), run('y3', [0.62, 0.66], 0.38, 0.3)]),
    S("2 · PASES CORTOS", ["NADA DE PELOTAZOS", "PASES CORTOS Y SEGUROS"],
      "Dos: nada de pelotazos. Pases cortos y seguros.",
      ball='y2',
      ev=[ghost('y2', [0.5, 0.12], 0.04, [0.5, 0.30]), pas('y2', 'y3', 0.3, 0.13), pas('y3', 'y5', 0.47, 0.13),
          pas('y5', 'y7', 0.64, 0.14)]),
    S("3 · ANIMA", ["UNA BRONCA HUNDE", "UN «¡VAMOS!» LEVANTA"],
      "Tres: una bronca hunde. Un ¡vamos! levanta.",
      ball='y5',
      ev=[bub('y4', '¡VAMOS!', 0.1, 0.3), bub('y6', '¡SEGUIMOS!', 0.35, 0.3), bub('y2', '¡BIEN!', 0.6, 0.35)]),
  ])

V['17_cinco_palabras'] = dict(
  hook=["5 PALABRAS", "QUE TE SALVAN", "EN UNA PACHANGA"],
  hook_voice="Cinco palabras que te salvan en una pachanga.",
  scenes=[
    S("1 · ¡SOLO!", ["TIENES TIEMPO", "CONTROLA TRANQUILO"],
      "¡Solo! Tienes tiempo, controla tranquilo.",
      ball='y6', focus=('y6', 'TÚ'),
      ev=[bub('y5', '¡SOLO!', 0.05, 0.45), drib('y6', [0.66, 0.48], 0.4, 0.3, 'none')]),
    S("2 · ¡HOMBRE!", ["TE VIENE UNO DETRÁS", "SUÉLTALA YA"],
      "¡Hombre! Te viene uno detrás, suéltala ya.",
      ball='y6', focus=('y6', 'TÚ'), pos={'r6': [0.74, 0.40]},
      ev=[run('r6', [0.69, 0.50], 0.08, 0.3, 'rrun'), bub('y5', '¡HOMBRE!', 0.12, 0.4), pas('y6', 'y5', 0.55, 0.15)]),
    S("3 · ¡GIRA!", ["NO TIENES A NADIE", "DATE LA VUELTA Y ENCARA"],
      "¡Gira! No tienes a nadie, date la vuelta y encara.",
      ball='y7', focus=('y7', 'TÚ'), pos={'y7': [0.5, 0.36], 'r7': [0.5, 0.75]},
      ev=[bub('y5', '¡GIRA!', 0.05, 0.4), drib('y7', [0.5, 0.20], 0.45, 0.3)]),
    S("4 · ¡MÍA!", ["VOY YO", "APÁRTATE"],
      "¡Mía! Voy yo, apártate.",
      ball='r5', focus=('y5', 'TÚ'), pos={'y3': [0.30, 0.66]},
      ev=[pas('r5', [0.36, 0.60], 0.04, 0.18), bub('y5', '¡MÍA!', 0.1, 0.45), run('y5', [0.36, 0.595], 0.3, 0.2),
          run('y3', [0.17, 0.74], 0.3, 0.25)]),
    S("5 · ¡SAL!", ["SUBIMOS TODOS", "JUNTOS"],
      "Y ¡sal! Subimos todos juntos.",
      ball='y6', focus=('y1', 'PORTERO'),
      ev=[bub('y1', '¡SAL!', 0.05, 0.45), run('y2', [0.5, 0.64], 0.25, 0.3), run('y3', [0.17, 0.60], 0.25, 0.3),
          run('y4', [0.83, 0.60], 0.25, 0.3)]),
  ])

PA = {'r7': [0.60, 0.64], 'y2': [0.48, 0.79], 'y4': [0.78, 0.76], 'r4': [0.86, 0.56]}
V['18_defender_en_pareja'] = dict(
  hook=["¿DEFIENDES CON ALGUIEN", "QUE NO CONOCES?", "¡ASÍ OS ENTENDÉIS!"],
  hook_voice="¿Defiendes con alguien que no conoces? ¡Así os entendéis!",
  scenes=[
    S("1 · UNO PRESIONA", ["EL MÁS CERCANO PRESIONA", "SOLO UNO, NO LOS DOS"],
      "Uno: el más cercano presiona. Solo uno, no los dos.",
      ball='r7', focus=('y2', 'TÚ'), pos=PA,
      ev=[run('y2', [0.57, 0.70], 0.08, 0.25), ghost('y4', 'r7', 0.45, [0.69, 0.70])]),
    S("2 · EL OTRO CUBRE", ["EL OTRO, DETRÁS", "Y EN DIAGONAL"],
      "Dos: el otro, detrás y en diagonal.",
      ball='r7', focus=('y4', 'TÚ'), pos=dict(PA, y2=[0.57, 0.70]),
      ev=[run('y4', [0.66, 0.80], 0.08, 0.3), tag('y2', 'PRESIONA', 0.45)]),
    S("3 · CAMBIO DE PAPELES", ["SI EL BALÓN CAMBIA DE LADO", "CAMBIÁIS LOS PAPELES"],
      "Tres: si el balón cambia de lado, cambiáis los papeles.",
      ball='r7', focus=('y4', 'TÚ'), pos=dict(PA, y2=[0.57, 0.70], y4=[0.66, 0.80]),
      ev=[pas('r7', 'r4', 0.06, 0.2), run('y4', [0.82, 0.62], 0.3, 0.25), run('y2', [0.70, 0.74], 0.32, 0.25),
          tag('y2', 'CUBRE', 0.62)]),
  ])

SB = {'y3': [0.0, 0.42], 'y5': [0.24, 0.46], 'r3': [0.30, 0.62], 'r5': [0.45, 0.60]}
V['19_saque_de_banda'] = dict(
  hook=["EL SAQUE DE BANDA", "QUE NADIE APROVECHA", "¡HAZ ESTO!"],
  hook_voice="El saque de banda que nadie aprovecha. ¡Haz esto!",
  scenes=[
    S("1 · SÁCALA RÁPIDO", ["SÁCALA RÁPIDO", "ANTES DE QUE SE COLOQUEN"],
      "Uno: sácala rápido, antes de que se coloquen.",
      ball='y3', focus=('y3', 'TÚ'), pos=SB,
      ev=[pas('y3', 'y5', 0.12, 0.15), run('r3', [0.24, 0.52], 0.2, 0.5, 'none'), drib('y5', [0.28, 0.30], 0.4, 0.3)]),
    S("2 · AL LIBRE", ["NO AL QUE MÁS GRITA", "AL QUE ESTÁ LIBRE"],
      "Dos: no al que más grita, al que está libre.",
      ball='y3', focus=('y3', 'TÚ'), pos=dict(SB, y7=[0.22, 0.33], r2=[0.25, 0.30], y5=[0.30, 0.50]),
      ev=[bub('y7', '¡AQUÍ, AQUÍ!', 0.04, 0.4), ghost('y3', 'y7', 0.3, [0.22, 0.32]), pas('y3', 'y5', 0.55, 0.18)]),
    S("3 · ENTRA RÁPIDO", ["DESPUÉS DE SACAR", "ENTRA RÁPIDO AL CAMPO"],
      "Tres: después de sacar, entra rápido al campo.",
      ball='y3', focus=('y3', 'TÚ'), pos=SB,
      ev=[pas('y3', 'y5', 0.06, 0.15), run('y3', [0.16, 0.30], 0.28, 0.3), pas('y5', 'y3', 0.66, 0.15)]),
  ])

for k, v in V.items():
    v['id'] = k
    v['cta_voice'] = CTA_VOICE

if __name__ == '__main__':
    json.dump(V, open('/home/claude/eng/specs.json', 'w'), ensure_ascii=False, indent=1)
    # voice paragraphs
    takes = {k: [v['hook_voice']] + [s['voice'] for s in v['scenes']] + [v['cta_voice']] for k, v in V.items()}
    json.dump(takes, open('/home/claude/eng/takes_v3.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in V.items():
        for s in v['scenes']:
            for l in s['sub']:
                if len(l) > 27: print('LONG', k, l, len(l))
    print(len(V), 'videos')
