from pptx import Presentation

prs = Presentation('reports/presentation/Nhom12_BaoCao_Slides.pptx')
print(f'Total slides: {len(prs.slides)}')
print(f'Slide dimensions: {prs.slide_width.inches:.3f} x {prs.slide_height.inches:.3f}')

all_contained = True
for s_idx, slide in enumerate(prs.slides, 1):
    cards = []
    pics = []
    for shp in slide.shapes:
        if shp.shape_type == 1: # auto shape
            # Exclude full-slide background shape
            if shp.width.inches > 13.0 and shp.height.inches > 7.0:
                continue
            cards.append(shp)
        elif shp.shape_type == 13: # picture
            pics.append(shp)
    
    print(f'Slide {s_idx:2d}: {len(slide.shapes)} shapes | {len(cards)} card shapes | {len(pics)} pictures')
    
    for p_i, pic in enumerate(pics):
        pl, pt, pw, ph = pic.left.inches, pic.top.inches, pic.width.inches, pic.height.inches
        pr, pb = pl + pw, pt + ph
        
        found = False
        for card in cards:
            cl, ct, cw, ch = card.left.inches, card.top.inches, card.width.inches, card.height.inches
            cr, cb = cl + cw, ct + ch
            if cl <= pl + 0.01 and ct <= pt + 0.01 and pr <= cr + 0.01 and pb <= cb + 0.01:
                pad_l = pl - cl
                pad_r = cr - pr
                pad_t = pt - ct
                pad_b = cb - pb
                print(f'   -> Picture {p_i+1} [{pw:.2f}x{ph:.2f}] INSIDE card [{cw:.2f}x{ch:.2f}]')
                print(f'      Paddings: left={pad_l:.2f}", right={pad_r:.2f}", top={pad_t:.2f}", bot={pad_b:.2f}"')
                found = True
                break
        if not found:
            print(f'   [ERROR] Picture {p_i+1} NOT INSIDE ANY CONTAINER CARD! Bounds: L={pl:.2f}, T={pt:.2f}, R={pr:.2f}, B={pb:.2f}')
            all_contained = False

if all_contained:
    print('\n>>> ALL 100% PICTURES/TABLES STRICTLY INSIDE CONTAINER CARDS! <<<')
else:
    print('\n>>> ERROR: SOME PICTURES ARE OUTSIDE CARDS! <<<')
